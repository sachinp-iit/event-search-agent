# models/embedding/embedding_loader.py

from sentence_transformers import SentenceTransformer

from config.settings import settings


# ================================================
# EMBEDDING MODEL LOADER
# ================================================

_embedding_model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)


# Get Embedding Model

async def get_embedding_model() -> SentenceTransformer:
    """
    Returns shared embedding model instance.
    """
    
    return _embedding_model