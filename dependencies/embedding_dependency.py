# dependencies/embedding_dependency.py

from sentence_transformers import SentenceTransformer

from models.embedding.embedding_loader import get_embedding_model


# ================================================
# EMBEDDING MODEL DEPENDENCY
# ================================================

async def embedding_model_dependency() -> SentenceTransformer:
    """
    Dependency injection provider for shared embedding model.
    """
    
    embedding_model = await get_embedding_model()
    
    return embedding_model