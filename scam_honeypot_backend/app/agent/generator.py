import random
from app.memory.models import AgentStrategy, ConversationState, Message
from app.agent.persona import PersonaEngine
from app.core.config import settings
from google import genai

class LLMGenerator:
    def __init__(self):
        self.persona = PersonaEngine()
        self.client = None
        if settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def generate_reply(self, state: ConversationState, strategy: AgentStrategy, last_user_msg: str) -> str:
        # Fallback if no API key is provided
        if not self.client:
            return f"[MOCK] (No API Key) {random.choice(self.persona.profile['catchphrases'])}"

        try:
            # Build history for context
            # We filter for the last 10 turns to keep context window manageable
            history_context = []
            for msg in state.history[-10:]:
                role = "user" if msg.role == "user" else "model"
                history_context.append({
                    "role": role, 
                    "parts": [{"text": msg.content}]
                })

            # Construct dynamic system instruction based on Strategy
            system_instruction = self.persona.get_system_prompt()
            system_instruction += f"\n\nCURRENT STRATEGY: {strategy.upper()}"
            system_instruction += "\nINSTRUCTION: "
            
            if strategy == AgentStrategy.PASSIVE:
                system_instruction += "Act confused, ask clarifying questions, do not commit to anything yet."
            elif strategy == AgentStrategy.ENGAGED:
                system_instruction += "Act interested. Ask how to proceed. Pretend you want to send money."
            elif strategy == AgentStrategy.VULNERABLE:
                system_instruction += "Act scared or overwhelmed by technology. Apologize profusely."
            elif strategy == AgentStrategy.STALLING:
                system_instruction += "Create delays. Make up excuses (internet slow, cat on keyboard, finding glasses)."
            
            # Call Gemini 2.0 Flash (free tier equivalent/fastest)
            # Note: "gemini-2.0-flash-exp" is often the ID for the latest/fastest, 
            # or "gemini-1.5-flash". Using "gemini-2.0-flash" as requested (or closest available).
            # If 2.0 is not available in the SDK yet, we fall back to 1.5-flash.
            # Using 'gemini-2.0-flash' as specific 2.0 request.
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=history_context,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.7,
                }
            )
            
            return response.text
            
        except Exception as e:
            return f"[ERROR] Gemini API Failed: {str(e)}"
