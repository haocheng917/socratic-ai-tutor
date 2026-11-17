
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from socratic_ai_tutor.config import SECRET_KEY, JWT_ALGORITHM
from socratic_ai_tutor.database import get_db
import jwt
from jwt import PyJWTError

from socratic_ai_tutor.repository.user import UserRepository

security = HTTPBearer()


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=7)

    to_encode = {"sub": str(user_id), "exp": expire}

    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get('sub'))
    except (PyJWTError, TypeError):
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录",
                            headers={"WWW-Authenticate": "Bearer"})

    user = await UserRepository.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
