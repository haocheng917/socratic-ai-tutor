from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from socratic_ai_tutor.models import User


class UserRepository:
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        result = await db.execute(select(User)
                                  .options(selectinload(User.sessions)).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_name(db: AsyncSession, username: str):
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(db: AsyncSession, username: str, hashed_password: str):
        user = User(username=username, password=hashed_password)
        db.add(user)
        await db.flush()
        await db.commit()
        return user.id
