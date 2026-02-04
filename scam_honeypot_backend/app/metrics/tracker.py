from app.memory.models import ConversationState

class MetricsTracker:
    @staticmethod
    def update_metrics(state: ConversationState):
        # Update session duration, etc.
        # This is simple for now as turn_count is already in state
        pass
