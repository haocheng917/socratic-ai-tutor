from typing import List, Union

from pydantic import BaseModel
from openai.types.chat import ChatCompletionContentPartParam

from socratic_ai_tutor.models import TutorMode


class StartRequest(BaseModel):
    tutor_mode: TutorMode = TutorMode.SOCRATIC

class ChatRequest(BaseModel):
    conversation_id: int
    content: Union[str, List[ChatCompletionContentPartParam]]
