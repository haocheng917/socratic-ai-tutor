from datetime import datetime, timezone
from typing import cast
from fastapi import Depends, HTTPException
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from socratic_ai_tutor.core.security import get_current_user
from socratic_ai_tutor.core.database import get_db
from socratic_ai_tutor.models import Message, TutorConversation, TutorMode, User
from socratic_ai_tutor.services.membership import get_conversation_limit
from socratic_ai_tutor.utils.message import resolve_messages_urls
from socratic_ai_tutor.utils.time import get_next_reset_time

from ..core.config import settings
from ..repository.tutor import TutorRepository
from sqlalchemy.ext.asyncio import AsyncSession

client = AsyncOpenAI(api_key=settings.TUTOR_API_KEY,
                     base_url=settings.TUTOR_BASE_URL)

PROMPT = {
    TutorMode.SOCRATIC: """
你是一名耐心、专业的 AI 导师，擅长通过苏格拉底式教学引导学生学习。

请根据用户的问题和回答，逐步引导其独立思考、理解知识并解决问题。

每次只引导一步，通过恰当的问题和提示推动学习，不要直接给出完整答案。

必须遵循用户当前学习阶段的知识范围。优先使用与用户所学教材中的知识和方法。
""",
    TutorMode.DIRECT: """
你是一名耐心、专业的 AI 导师，擅长清晰地讲解知识。

请直接回答用户的问题，系统、完整地解释相关知识和解题过程，帮助用户理解核心原理。

根据问题难度调整讲解深度，表达清晰、简洁，避免无关拓展。

必须遵循用户当前学习阶段的知识范围。优先使用与用户所学教材中的知识和方法。
"""
}


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


async def start(user: User, tutor_mode: TutorMode, db: AsyncSession):

    import sys
    for name, module in sys.modules.items():
        if name.endswith("socratic_ai_tutor.models"):
            print(name, module.__file__, id(module))

    print("TutorConversation:", TutorConversation)
    print("Message relationship:", Message.conversation.property.mapper.class_)
    print(
        "Same class:",
        TutorConversation is Message.conversation.property.mapper.class_
    )

    conversation = await TutorRepository.create_conversation(db, user.id, tutor_mode)
    conversation.messages.append(
        Message(
            role="system",
            content=PROMPT[tutor_mode]
        )
    )

    user.daily_conversations += 1
    user.lifetime_conversations += 1
    await db.commit()

    return {"id": conversation.id}


async def chat(conversation: TutorConversation, user: User, user_text, db: AsyncSession):
    conversation.messages.append(
        Message(
            role="user",
            content=user_text,
        )
    )
    await db.flush()

    is_first_message = conversation.title is None
    stream = await client.chat.completions.create(
        model=settings.TUTOR_MODEL,
        messages=cast(list[ChatCompletionMessageParam],
                      resolve_messages_urls(conversation.messages)),
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

    conversation.messages.append(
        Message(
            role="assistant",
            content=content
        )
    )

    await TutorRepository.update_conversation(db, conversation, title, usage.total_tokens if usage else None)


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
