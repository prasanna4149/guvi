from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime

class ConversationStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"

class AgentStrategy(str, Enum):
    PASSIVE = "passive"     # Listening, unsure
    ENGAGED = "engaged"     # Baiting
    STALLING = "stalling"   # Wasting time
    VULNERABLE = "vulnerable" # Pretending to fall for it
    REFUSAL = "refusal"     # Soft refusal to trigger urgency

class ExtractedIntel(BaseModel):
    type: str  # UPI, BANK_ACCOUNT, URL, PHONE
    value: str
    confidence: float
    turn_found: int

class Message(BaseModel):
    role: str # user, agent
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ConversationState(BaseModel):
    conversation_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    status: ConversationStatus = ConversationStatus.ACTIVE
    
    history: List[Message] = []
    
    # Analysis State
    scam_score: float = 0.0
    is_scam_confirmed: bool = False
    
    # Agent State
    current_strategy: AgentStrategy = AgentStrategy.PASSIVE
    risk_level: float = 0.0 # 0.0 to 1.0 (How suspicious the scammer is)
    
    # Intel
    extracted_data: List[ExtractedIntel] = []
    
    # Metrics
    turn_count: int = 0
