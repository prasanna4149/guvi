from pydantic import BaseModel
from typing import Optional, List, Any

class MessageRequest(BaseModel):
    conversation_id: str
    message: str
    timestamp: Optional[str] = None

class MessageResponse(BaseModel):
    conversation_id: str
    agent_reply: str
    metadata: dict
    timestamp: str
