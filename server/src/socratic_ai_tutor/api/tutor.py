import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from socratic_ai_tutor.core.security import get_current_user
from socratic_ai_tutor.models import TutorMode, User
from socratic_ai_tutor.repository.tutor import TutorRepository
from socratic_ai_tutor.services.membership import MEMBERSHIP_PLANS

from ..schema.tutor import ChatRequest, StartRequest
from ..database import get_db
from ..services import tutor

router = APIRouter(prefix="/tutor", tags=["Tutor"])


@router.post('/start')
async def start(req: StartRequest, db: AsyncSession = Depends(get_db),
                user: User = Depends(tutor.check_conversation_quota)):
    return await tutor.start(user, req.tutor_mode, db)


@router.post('/chat')
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db),
               user: User = Depends(get_current_user)):
    conversation = await TutorRepository.get_conversation(db, req.conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="会话不存在")
    elif conversation.user_id != user.id:
        raise HTTPException(status_code=403, detail="无权访问该对话")
    elif conversation.context_tokens >= int(MEMBERSHIP_PLANS[user.membership_plan].get('conversation_token_limit', 128000000)):
        raise HTTPException(status_code=429, detail="对话长度超过限制，升级会员以获得更大限制")

    async def event_generator():
        async for event in tutor.chat(
            conversation, user, req.content, db
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
