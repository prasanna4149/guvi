from app.memory.models import ConversationState, Message
from app.detection.analyzer import ScamAnalyzer
from app.agent.strategy import StrategySelector
from app.agent.belief import BeliefSystem
from app.agent.generator import LLMGenerator
from app.memory.store import memory_store

class AgentController:
    def __init__(self):
        self.generator = LLMGenerator()

    async def process_turn(self, conversation_id: str, user_text: str) -> tuple[str, dict]:
        # 1. Load State
        state = await memory_store.get_conversation(conversation_id)
        if not state:
            state = await memory_store.create_conversation(conversation_id)

        # 2. Update History
        state.history.append(Message(role="user", content=user_text))
        state.turn_count += 1

        # 3. Detection (if not already confirmed)
        meta = {"scam_detected": state.is_scam_confirmed}
        if not state.is_scam_confirmed:
            detection = ScamAnalyzer.analyze(user_text)
            state.scam_score = detection.score
            state.is_scam_confirmed = detection.is_scam
            meta["scam_detected"] = detection.is_scam
            meta["detection_reasons"] = detection.reasons
        
        # 4. Agent Logic (Only if scam or debugging)
        # Even if not scam, we might reply generically or echo. 
        # For this honeypot, we assume we want to respond to see if it BECOMES a scam, 
        # or we might respond properly if it IS a scam. 
        # Requirement: "Detection only unlocks agent mode internally".
        # Implication: If not detected, maybe standard reply or nothing? 
        # Let's assume we ALWAYS reply but the 'Strategy' changes.
        
        # Update Belief/Risk
        belief = BeliefSystem(state)
        belief.update_risk(user_text)
        
        # Select Strategy
        strategy = StrategySelector.select_next_strategy(state)
        state.current_strategy = strategy
        
        # Generate Reply
        reply_text = await self.generator.generate_reply(state, strategy, user_text)
        
        # Update History with Reply
        state.history.append(Message(role="agent", content=reply_text))
        
        # Save State
        await memory_store.save_conversation(state)
        
        meta["strategy"] = strategy
        meta["turn"] = state.turn_count
        
        return reply_text, meta
