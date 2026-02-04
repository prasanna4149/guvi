from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agentic Honey-Pot"
    API_V1_STR: str = "/api/v1"
    API_KEY: str = "secret-honey-key"
    
    # Detection Thresholds
    SCAM_THRESHOLD: float = 0.7
    
    # Agent Settings
    MAX_TURNS: int = 20
    GEMINI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
