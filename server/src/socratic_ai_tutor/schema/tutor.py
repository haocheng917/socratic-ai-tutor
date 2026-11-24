from typing import List, Union

from pydantic import BaseModel
from openai.types.chat import ChatCompletionContentPartParam

class ChatRequest(BaseModel):
    conversation_id: int
    content: Union[str, List[ChatCompletionContentPartParam]]
