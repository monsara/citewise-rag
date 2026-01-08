"""
Configuration settings for CiteWise RAG ML Service
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Database connections
    weaviate_url: str = "http://localhost:8080"
    postgres_url: str = "postgresql://citewise:citewise_dev_password@localhost:5432/citewise"
    
    # LLM Provider settings
    llm_provider: Literal["ollama", "openai", "groq"] = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    groq_api_key: str = ""
    
    # Embedding Provider settings
    embedding_provider: Literal["local", "openai"] = "local"
    local_embedding_model: str = "all-MiniLM-L6-v2"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # RAG parameters
    default_top_k: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_chunks_per_document: int = 3
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = [
        "http://localhost:3000",
        "https://citewise-web.onrender.com"
    ]


# Global settings instance
settings = Settings()
