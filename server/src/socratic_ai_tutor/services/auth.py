from sqlalchemy.ext.asyncio import AsyncSession

from socratic_ai_tutor.core.security import create_access_token, get_password_hash, verify_password
from socratic_ai_tutor.repository.user import UserRepository


async def login(username: str, password: str, db: AsyncSession):
    user = await UserRepository.get_user_by_name(db, username)

    if not user or not verify_password(password, user.password):
        raise ValueError("用户名或密码错误")

    return create_access_token(user.id)


async def register(username: str, password: str, db: AsyncSession):
    if await UserRepository.get_user_by_name(db, username):
        raise ValueError("用户名已存在")

    user_id = await UserRepository.create_user(
        db, username, get_password_hash(password))

    return create_access_token(user_id)
