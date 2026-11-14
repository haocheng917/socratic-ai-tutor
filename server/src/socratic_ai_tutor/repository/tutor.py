from sqlalchemy import select

from ..models import TutorSession
from sqlalchemy.ext.asyncio import AsyncSession

class TutorRepository:
    @staticmethod
    async def create_session(db: AsyncSession, messages: list):
        tutor_session = TutorSession(messages=messages)
        db.add(tutor_session)
        await db.flush()
        await db.commit()
        return tutor_session.id

    @staticmethod
    async def get_messages(db: AsyncSession, id: int):
        result = await db.scalar(select(TutorSession).where(TutorSession.id == id))
        if result is None:
            return []
        return result.messages

    @staticmethod
    async def update_messages(db: AsyncSession, id: int, messages: list):
        session = await db.scalar(select(TutorSession).where(TutorSession.id == id))
        if session:
            session.messages = messages
            await db.commit()