from sqlalchemy import select

from ..models import TutorConversation, User
from sqlalchemy.ext.asyncio import AsyncSession


class TutorRepository:
    @staticmethod
    async def create_conversation(db: AsyncSession, user_id: int, messages: list):
        tutor_conversation = TutorConversation(
            messages=messages,
            user_id=user_id,
        )
        db.add(tutor_conversation)
        await db.flush()
        await db.commit()
        return tutor_conversation.id

    @staticmethod
    async def get_conversation(db: AsyncSession, id: int):
        return await db.scalar(select(TutorConversation).where(TutorConversation.id == id))

    @staticmethod
    async def update_messages(db: AsyncSession, conversation: TutorConversation, messages: list, title: str | None = None):
        conversation.messages = messages
        if title:
            conversation.title = title
        await db.commit()
