"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "AI Query Router"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Redis
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    cache_ttl: int = 3600
    
    # Kafka
    kafka_bootstrap_servers: str = "kafka:9092"
    kafka_topic: str = "query_events"
    
    # PostgreSQL
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "ai_router"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    
    # Groq (FREE and FAST)
    groq_api_key: Optional[str] = None
    use_groq: bool = False
    groq_simple_model: str = "llama-3.1-8b-instant"
    groq_medium_model: str = "llama-3.3-70b-versatile"
    groq_complex_model: str = "openai/gpt-oss-120b"
    
    # Together AI (FREE - Great as fallback)
    together_api_key: Optional[str] = None
    use_together_as_fallback: bool = True
    together_simple_model: str = "meta-llama/Llama-3.2-3B-Instruct-Turbo"
    together_medium_model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    together_complex_model: str = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    
    # Fallback configuration
    enable_fallback: bool = True
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    # Query Classification
    simple_query_max_words: int = 10
    medium_query_max_words: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


# Global settings instance
settings = Settings()
