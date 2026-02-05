import random
from app.memory.models import AgentStrategy, ConversationState, Message
from app.agent.persona import PersonaEngine
from app.core.config import settings
from groq import Groq

class LLMGenerator:
    def __init__(self):
        self.persona = PersonaEngine()
        self.client = None
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)

    async def generate_reply(self, state: ConversationState, strategy: AgentStrategy, last_user_msg: str) -> str:
        # Fallback if no API key is provided
        if not self.client:
            return f"[MOCK] (No Groq API Key) {random.choice(self.persona.profile['catchphrases'])}"

        try:
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
            
            # Build history for context (Groq/OpenAI format)
            messages = [{"role": "system", "content": system_instruction}]
            
            # Add last 10 turns
            for msg in state.history[-10:]:
                # Map 'agent' role to 'assistant' for OpenAI/Groq spec
                role = "assistant" if msg.role == "agent" else "user"
                messages.append({
                    "role": role, 
                    "content": msg.content
                })

            # Call Groq API
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                temperature=1,
                max_completion_tokens=8192,
                top_p=1,
                stream=False, # Keeping it simple for now (user example had stream=True but our code expects string return)
                stop=None
            )
            
            # Return content
            return completion.choices[0].message.content or ""
            
        except Exception as e:
            return f"[ERROR] Groq API Failed: {str(e)}"
