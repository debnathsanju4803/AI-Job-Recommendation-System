"""
Configuration settings for the application
"""
import os
from pathlib import Path
from typing import Optional, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    """Application settings"""
    
    # Project paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models"
    
    # LLM Settings (Ollama - free, local)
    LLM_PROVIDER: str = "ollama"  # Options: ollama, huggingface
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"  # or mistral, codellama, etc.
    
    # HuggingFace Settings (alternative)
    HF_MODEL: str = "microsoft/Phi-3-mini-4k-instruct"
    HF_DEVICE: str = "cpu"  # or cuda if GPU available
    
    # Vector Database Settings (Chroma - free, local)
    VECTOR_DB_PROVIDER: str = "chroma"  # Options: chroma, qdrant
    CHROMA_PERSIST_DIR: str = str(DATA_DIR / "chroma_db")
    CHROMA_COLLECTION_NAME: str = "job_descriptions"
    
    # Qdrant Settings (alternative)
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    
    # Embeddings Settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"  # Free, local
    EMBEDDING_DIMENSION: int = 384
    
    # Job Search Settings
    MAX_JOBS_PER_SEARCH: int = 50
    JOB_SOURCES: list = ["arbeitnow", "remoteok", "indeed"]  # Free sources (github deprecated)
    
    # Scraping Settings
    SCRAPING_DELAY: float = 1.0  # Delay between requests (seconds)
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "AI Resume Parser & Job Recommender"
    API_VERSION: str = "1.0.0"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    # Redis (optional, for caching)
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: int = 6379
    REDIS_TTL: int = 3600  # 1 hour
    
    @field_validator("JOB_SOURCES", mode="before")
    @classmethod
    def parse_job_sources(cls, v: Union[str, list]) -> list:
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v
    
    @field_validator("DATA_DIR", mode="after")
    @classmethod
    def ensure_data_dir(cls, v: Path) -> Path:
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
