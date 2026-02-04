from app.memory.models import ConversationState, AgentStrategy

class StrategySelector:
    @staticmethod
    def select_next_strategy(state: ConversationState) -> AgentStrategy:
        # State Machine Logic
        
        # If we have gathered a lot of intel, maybe start stalling to keep them on hook or close
        if len(state.extracted_data) > 3:
            return AgentStrategy.STALLING
            
        # If risk is high, play dumb/vulnerable to lower suspicion
        if state.risk_level > 0.6:
            return AgentStrategy.VULNERABLE
            
        # Default flow: Passive -> Engaged
        if state.turn_count < 2:
            return AgentStrategy.PASSIVE
        else:
            return AgentStrategy.ENGAGED
