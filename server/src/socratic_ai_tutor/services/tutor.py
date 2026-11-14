from typing import cast
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from socratic_ai_tutor.utils.message import resolve_messages_urls

from .oss import StorageService
from ..config import API_KEY
from ..repository.tutor import TutorRepository
from sqlalchemy.ext.asyncio import AsyncSession


client = AsyncOpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")


async def start(image_bytes: bytes, image_ext: str, db: AsyncSession):
    key = StorageService.upload_image(image_bytes, image_ext)

    messages = [
        {
            "role": "system",
            "content": "以初中数学老师的身份向用户讲解这道题目，使用初中方法，返回格式为标准的Markdown，通过与用户不断的对话和提问，苏格拉底式的引导用户解题，每次引导一步",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": key},
                },
            ],
        },
    ]

    response = await client.chat.completions.create(
        model="deepseek-flash",
        messages=cast(list[ChatCompletionMessageParam],
                      resolve_messages_urls(messages)),
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
    )

    content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": content})
    session_id = await TutorRepository.create_session(db, messages)
    print(response.usage)

    return {"id": session_id, "content": content}


async def chat(session_id: int, user_text: str, db: AsyncSession):
    messages = await TutorRepository.get_messages(db, session_id)
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

    await TutorRepository.update_messages(db, session_id, messages)

    return {"id": session_id, "content": content}
