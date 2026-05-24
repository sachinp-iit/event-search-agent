# dependencies/qdrant_dependency.py

from qdrant_client import AsyncQdrantClient

from vector_db.qdrant_client import get_qdrant_client


# =========================================================
# QDRANT DEPENDENCY PROVIDER
# =========================================================

async def qdrant_client_dependency() -> AsyncQdrantClient:
    """
    Dependency injection provider for shared async Qdrant client.
    """
    
    qdrant_client = await get_qdrant_client()
    
    return qdrant_client
    