# config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =====================================================
    # FASTAPI APPLICATION
    # =====================================================

    APP_NAME: str
    APP_VERSION: str
    APP_HOST: str
    APP_PORT: int
    DEBUG: bool

    # =====================================================
    # OPENROUTER CONFIGURATION
    # =====================================================

    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_MODEL: str
    OPENROUTER_HEADER_HTTP_REFERER: str
    OPENROUTER_HEADER_HTTP_X_TITLE: str

    # =====================================================
    # QDRANT VECTOR DATABASE
    # =====================================================

    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str
    
    
    # =====================================================
    # SQL SERVER DATABASE
    # =====================================================
    
    SQL_SERVER_CONNECTION_STRING: str

    # =====================================================
    # EMBEDDING + RERANKING MODELS
    # =====================================================

    EMBEDDING_MODEL: str
    RERANKER_MODEL: str

    # =====================================================
    # MODERATION + NER MODELS
    # =====================================================

    TOXICITY_MODEL: str
    NER_MODEL: str

    # =====================================================
    # TRANSCRIPT PROCESSING
    # =====================================================

    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    TOP_K_RESULTS: int
    INGESTION_BATCH_SIZE: int
    MAX_CONCURRENT_BATCHES: int
    
    # =========================================================
    # RAW TRANSCRIPT DIRECTORY
    # =========================================================
    
    RAW_TRANSCRIPTS_DIRECTORY: str

    # =====================================================
    # LANGSMITH OBSERVABILITY
    # =====================================================

    LANGSMITH_TRACING_V2: bool
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str

    # =====================================================
    # LANGFUSE OBSERVABILITY
    # =====================================================

    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_HOST: str

    # =====================================================
    # LOGGING
    # =====================================================

    LOG_LEVEL: str
    
    # =====================================================
    # METADATA - INDEXED FIELDS
    # =====================================================    
    
    EVENT_NAME: str
    EVENT_TOPIC: str
    SPEAKER_NAME: str
    EVENT_DATE: str
    EVENT_COMPANY: str
    EVENT_LOCATION: str
    DOMAIN: str
    CATEGORY: str
    
    # =========================================================
    # EMBEDDING CONFIGURATION
    # =========================================================

    EMBEDDING_DIMENSION: int

    # =====================================================
    # Pydantic Settings Config
    # =====================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    

# =========================================================
# GLOBAL SETTINGS INSTANCE
# =========================================================

settings = Settings()