from datetime import datetime, timezone
from typing import cast
from fastapi import Depends, HTTPException
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from socratic_ai_tutor.core.security import get_current_user
from socratic_ai_tutor.database import get_db
from socratic_ai_tutor.models import User
from socratic_ai_tutor.services.membership import get_conversation_limit
from socratic_ai_tutor.utils.message import resolve_messages_urls
from socratic_ai_tutor.utils.time import get_next_reset_time

from ..config import API_KEY
from ..repository.tutor import TutorRepository
from sqlalchemy.ext.asyncio import AsyncSession

client = AsyncOpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")


async def check_conversation_quota(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    limit, limit_type = get_conversation_limit(user)

    if limit_type == 'lifetime':
        if user.lifetime_conversations >= limit:
            raise HTTPException(403, "对话次数额度已用完")
    elif limit_type == 'daily':
        now = datetime.now(timezone.utc)
        if user.daily_reset_at is None or now >= user.daily_reset_at:
            user.daily_reset_at = get_next_reset_time(now)
            user.daily_conversations = 0
            await db.flush()
        if user.daily_conversations >= limit:
            raise HTTPException(403, "对话次数额度已用完")

    return user


async def start(user: User, db: AsyncSession):
    messages = [
        {
            "role": "system",
            "content": "以初中数学老师的身份向用户讲解这道题目，使用初中方法，返回格式为标准的Markdown，通过与用户不断的对话和提问，苏格拉底式的引导用户解题，每次引导一步",
        },
    ]

    conversation_id = await TutorRepository.create_conversation(db, user.id, messages)

    user.daily_conversations += 1
    user.lifetime_conversations += 1
    await db.commit()

    return {"id": conversation_id}


async def chat(conversation_id: int, user: User, user_text, db: AsyncSession):
    conversation = await TutorRepository.get_conversation(db, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="会话不存在")
    elif conversation.user_id != user.id:
        raise HTTPException(status_code=403, detail="无权访问该对话")

    messages = list(conversation.messages)
    messages.append({"role": "user", "content": user_text})

    await TutorRepository.update_messages(db, conversation, messages)

    is_first_message = conversation.title is None
    stream = await client.chat.completions.create(
        model="deepseek-flash",
        messages=cast(list[ChatCompletionMessageParam],
                      resolve_messages_urls(messages)),
        reasoning_effort="high",
        stream=True,
        extra_body={
            "thinking": {"type": "enabled"},
            "title": {"enabled": is_first_message}
        },
    )

    content = ""
    title = None
    usage = None
    async for chunk in stream:
        delta = chunk.choices[0].delta

        if delta.content:
            content += delta.content
            yield {
                "type": "content",
                "content": delta.content
            }

        if chunk.usage:
            usage = chunk.usage

        if hasattr(delta, "title"):
            title = delta.title  # type: ignore
            yield {
                "type": "title",
                "title": title
            }

    messages.append({"role": "assistant", "content": content})

    await TutorRepository.update_messages(db, conversation, messages, title)


async def get_history(conversation_id: int, user: User, db: AsyncSession):
    conversation = await TutorRepository.get_conversation(db, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="会话不存在")
    elif conversation.user_id != user.id:
        raise HTTPException(status_code=403, detail="无权访问该对话")
    return resolve_messages_urls(conversation.messages)


async def get_conversations(user: User):
    res = []
    for conversation in user.conversations:
        res.append({'id': conversation.id, 'title': conversation.title})
    return res
