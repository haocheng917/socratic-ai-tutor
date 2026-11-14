from fastapi import APIRouter, Depends, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ..schema.tutor import ChatRequest
from ..database import get_db
from ..services import tutor

router = APIRouter(prefix="/tutor", tags=["Tutor"])


@router.post('/start')
async def start(file: UploadFile, db: AsyncSession = Depends(get_db)):
    image_bytes = await file.read()
    return await tutor.start(image_bytes, db)


@router.post('/chat')
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    return await tutor.chat(req.session_id, req.user_text, db)
