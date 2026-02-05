from app.memory.models import ConversationState
from datetime import datetime

class MetricsTracker:
    @staticmethod
    def update_metrics(state: ConversationState):
        """
        Updates conversation metrics based on the current state.
        This calculates session duration and ensures turn counts are accurate.
        """
        # Update timestamp
        state.last_updated = datetime.now()
        
        # Calculate duration if needed (not stored explicitly in model yet, but good for logic)
        duration = (state.last_updated - state.created_at).total_seconds()
        
        # Ensure turn count matches history (safe-guard)
        # We divide by 2 assuming User-Agent pairs, or just count total messages
        # 'turn_count' usually implies round trips.
        state.turn_count = len(state.history) // 2
