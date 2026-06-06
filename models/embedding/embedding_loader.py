# models/embedding/embedding_loader.py

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.embeddings import Embeddings

from config.settings import settings


# ================================================
# EMBEDDING MODEL LOADER
# ================================================

_embedding_model = HuggingFaceEmbeddings (
    model_name = settings.EMBEDDING_MODEL,
    encode_kwargs = {
        "normalize_embeddings": True
    }
)

# Get Embedding Model
async def get_embedding_model() -> Embeddings:
    """
    Returns shared embedding model instance.
    """
    
    return _embedding_model