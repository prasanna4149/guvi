from app.memory.models import ConversationState

class BeliefSystem:
    def __init__(self, state: ConversationState):
        self.state = state

    def update_risk(self, message: str) -> float:
        # Simple logic: Short messages or aggressive punctuation increases risk
        risk_delta = 0.0
        if "!!!" in message:
            risk_delta += 0.1
        if len(message) < 5:
            risk_delta += 0.05
        
        new_risk = min(self.state.risk_level + risk_delta, 1.0)
        self.state.risk_level = new_risk
        return new_risk

    def is_compromised(self) -> bool:
        return self.state.risk_level > 0.8
