import os

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from socratic_ai_tutor.core.security import get_current_user
from socratic_ai_tutor.models import User

from ..schema.tutor import ChatRequest, StartRequest
from ..database import get_db
from ..services import tutor

router = APIRouter(prefix="/tutor", tags=["Tutor"])


@router.post('/start')
async def start(req: StartRequest, db: AsyncSession = Depends(get_db),
                user: User = Depends(get_current_user)):
    content_dict = req.model_dump()["content"]
    return await tutor.start(content_dict, user.id, db)


@router.post('/chat')
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db),
               user: User = Depends(get_current_user)):
    return await tutor.chat(req.session_id, req.content, db)

router.get("/history/{session_id}")


async def get_history(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    messages = await tutor.get_history(session_id, db)

    return {"session_id": session_id, "messages": messages}
