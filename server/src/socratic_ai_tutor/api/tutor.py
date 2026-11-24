import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from socratic_ai_tutor.core.security import get_current_user
from socratic_ai_tutor.models import User

from ..schema.tutor import ChatRequest
from ..database import get_db
from ..services import tutor

router = APIRouter(prefix="/tutor", tags=["Tutor"])


@router.post('/start')
async def start(db: AsyncSession = Depends(get_db),
                user: User = Depends(tutor.check_conversation_quota)):
    return await tutor.start(user, db)


@router.post('/chat')
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db),
               user: User = Depends(get_current_user)):
    async def event_generator():
        async for event in tutor.chat(
            req.conversation_id, user, req.content, db
        ):
            data = json.dumps(event, ensure_ascii=False)
            yield f"data: {data}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@router.get("/history/{conversation_id}")
async def get_history(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    messages = await tutor.get_history(conversation_id, user, db)

    return {"conversation_id": conversation_id, "messages": messages}


@router.get('/conversations')
async def get_conversations(
    user: User = Depends(get_current_user),
):
    return {'conversations': await tutor.get_conversations(user)}
