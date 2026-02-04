from typing import Dict, Optional
from app.memory.models import ConversationState

class MemoryStore:
    def __init__(self):
        # In a real production app, this would be Redis
        self._store: Dict[str, ConversationState] = {}

    async def get_conversation(self, conversation_id: str) -> Optional[ConversationState]:
        return self._store.get(conversation_id)

    async def save_conversation(self, state: ConversationState):
        self._store[state.conversation_id] = state

    async def create_conversation(self, conversation_id: str) -> ConversationState:
        state = ConversationState(conversation_id=conversation_id)
        self._store[conversation_id] = state
        return state

# Global instance
memory_store = MemoryStore()
