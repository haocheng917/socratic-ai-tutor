from sqlalchemy import select

from ..models import TutorSession, User
from sqlalchemy.ext.asyncio import AsyncSession


class TutorRepository:
    @staticmethod
    async def create_session(db: AsyncSession, title: str, user_id: int, messages: list):
        tutor_session = TutorSession(
            messages=messages, 
            title=title, 
            user_id=user_id,
            membership_plan='Free'
        )
        db.add(tutor_session)
        await db.flush()
        await db.commit()
        return tutor_session.id

    @staticmethod
    async def get_session(db: AsyncSession, id: int):
        return await db.scalar(select(TutorSession).where(TutorSession.id == id))

    @staticmethod
    async def update_messages(db: AsyncSession, session: TutorSession, messages: list):
        session.messages = messages
        await db.commit()
