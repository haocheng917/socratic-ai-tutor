from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from socratic_ai_tutor.core.security import get_current_user
from socratic_ai_tutor.core.database import get_db
from socratic_ai_tutor.models import User
from socratic_ai_tutor.schema.auth import UserLogin, UserMe, UserRegister
from ..services import auth


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post('/register')
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    try:
        token = await auth.register(data.username, data.password, db)
        return {"message": "注册成功", "access_token": token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        token = await auth.login(data.username, data.password, db)
        return {"access_token": token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/me', response_model=UserMe)
async def get_me(user: User = Depends(get_current_user)):
    return user