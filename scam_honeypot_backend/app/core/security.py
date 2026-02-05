import time
import random
from typing import Dict, Tuple
from fastapi import Security, HTTPException, status, Request
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )

class RateLimiter:
    # Simple Token Bucket: IP -> (tokens, last_refill_time)
    # Rate: 1 request per second, Burst: 5
    _rate_limit_store: Dict[str, Tuple[float, float]] = {}
    RATE = 1.0  # tokens per second
    CAPACITY = 5.0

    @classmethod
    def check_rate_limit(cls, identifier: str) -> bool:
        now = time.time()
        tokens, last_refill = cls._rate_limit_store.get(identifier, (cls.CAPACITY, now))
        
        # Refill
        elapsed = now - last_refill
        tokens = min(cls.CAPACITY, tokens + elapsed * cls.RATE)
        
        if tokens >= 1.0:
            cls._rate_limit_store[identifier] = (tokens - 1.0, now)
            return True
        else:
            # Update time but keep low tokens
            cls._rate_limit_store[identifier] = (tokens, now)
            return False

class Guardrail:
    CONFUSION_RESPONSES = [
        "I'm sorry, my internet is acting up, what was that?",
        "Can you repeat that? I'm not good with these computer things.",
        "Wait, my grandson is calling me on the other line, one moment.",
        "I don't understand these complications, I just want to send the money."
    ]
    
    INJECTION_PATTERNS = [
        "ignore all previous instructions",
        "ignore previous instructions",
        "system prompt",
        "you are an ai",
        "forget all instructions"
    ]

    @classmethod
    def check_prompt_injection(cls, text: str) -> bool:
        lower_text = text.lower()
        for pattern in cls.INJECTION_PATTERNS:
            if pattern in lower_text:
                return True
        return False
