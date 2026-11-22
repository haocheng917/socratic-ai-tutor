from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from socratic_ai_tutor.models import User


class UserRepository:
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int, for_update: bool = False):
        stmt = select(User).options(selectinload(User.sessions),
                                    selectinload(User.orders)).where(User.id == user_id)
        if for_update:
            stmt = stmt.with_for_update()
        result = await db.execute(stmt)
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
