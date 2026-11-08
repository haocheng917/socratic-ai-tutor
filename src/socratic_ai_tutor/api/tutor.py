from fastapi import APIRouter, UploadFile
from ..services import tutor

router = APIRouter(prefix="/tutor", tags=["Tutor"])

@router.post('/start')
async def start(file: UploadFile):
    image_bytes = await file.read()
    return tutor.solve(image_bytes)