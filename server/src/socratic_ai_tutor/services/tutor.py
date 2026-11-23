from typing import cast
from fastapi import HTTPException
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from socratic_ai_tutor.models import User
from socratic_ai_tutor.utils.message import resolve_messages_urls

from .oss import StorageService
from ..config import API_KEY
from ..repository.tutor import TutorRepository
from sqlalchemy.ext.asyncio import AsyncSession


client = AsyncOpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")


async def start(content, user_id: int, db: AsyncSession):
    messages = [
        {
            "role": "system",
            "content": "以初中数学老师的身份向用户讲解这道题目，使用初中方法，返回格式为标准的Markdown，通过与用户不断的对话和提问，苏格拉底式的引导用户解题，每次引导一步",
        },
        {
            "role": "user",
            "content": content
        },
    ]

    response = await client.chat.completions.create(
        model="deepseek-flash",
        messages=cast(list[ChatCompletionMessageParam],
                      resolve_messages_urls(messages)),
        reasoning_effort="high",
        extra_body={
            "thinking": {"type": "enabled"},
            "title": {"enabled": True}
        },
    )

    title = response.choices[0].message.model_dump().get("title") or "新会话"
    content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": content})
    conversation_id = await TutorRepository.create_conversation(db, title, user_id, messages)
    print(response.usage)

    return {"id": conversation_id, "content": content}


async def chat(conversation_id: int, user: User, user_text, db: AsyncSession):
    conversation = await TutorRepository.get_conversation(db, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="会话不存在")
    elif conversation.user_id != user.id:
        raise HTTPException(status_code=403, detail="无权访问该对话")

    messages = list(conversation.messages)
    messages.append({"role": "user", "content": user_text})

    response = await client.chat.completions.create(
        model="deepseek-flash",
        messages=cast(list[ChatCompletionMessageParam],
                      resolve_messages_urls(messages)),
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
    )

    content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": content})
    print(response.usage)

    await TutorRepository.update_messages(db, conversation, messages)

    return {"id": conversation_id, "content": content}


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
