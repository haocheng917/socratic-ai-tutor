from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..models import Message, TutorConversation, TutorMode
from sqlalchemy.ext.asyncio import AsyncSession


class TutorRepository:
    @staticmethod
    async def create_conversation(db: AsyncSession, user_id: int, tutor_mode: TutorMode):
        tutor_conversation = TutorConversation(
            user_id=user_id,
            tutor_mode=tutor_mode,
            messages=[]
        )
        db.add(tutor_conversation)
        await db.flush()
        await db.commit()
        return tutor_conversation

    @staticmethod
    async def get_conversation(db: AsyncSession, id: int):
        return await db.scalar(select(TutorConversation).options(selectinload(TutorConversation.messages)).where(TutorConversation.id == id))

    @staticmethod
    async def update_conversation(db: AsyncSession, conversation: TutorConversation, title: str | None, tokens: int | None = None):
        if tokens:
            conversation.context_tokens = tokens
        if title:
            conversation.title = title
        await db.commit()
