from datetime import datetime
from app.api.schemas import MessageResponse

class ResponseBuilder:
    @staticmethod
    def build(conversation_id: str, reply: str, meta: dict) -> MessageResponse:
        return MessageResponse(
            conversation_id=conversation_id,
            agent_reply=reply,
            metadata=meta,
            timestamp=datetime.now().isoformat()
        )
