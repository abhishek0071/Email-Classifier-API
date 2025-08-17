from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List          # ← add this line

class Settings(BaseSettings):
    ollama_url: str = "http://127.0.0.1:11434"
    default_model: str = "gemma3:1b"
    allowed_models: List[str] = Field(
        default_factory=lambda: ["gemma3:1b", "llama3:8b"]
    )
    max_tokens: int = 3000
    # Gunicorn / Uvicorn workers etc. can be set here or via env vars

    class Config:
        env_file = ".env"

settings = Settings()
