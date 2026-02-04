from app.memory.models import ConversationState

class QualityScorer:
    @staticmethod
    def calculate_score(state: ConversationState) -> float:
        score = 0.0
        for item in state.extracted_data:
            if item.type == "UPI": score += 10
            elif item.type == "URL": score += 5
            elif item.type == "PHONE": score += 5
        
        return score
