from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from socratic_ai_tutor.database import get_db
from socratic_ai_tutor.schema.auth import UserLogin, UserRegister
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
