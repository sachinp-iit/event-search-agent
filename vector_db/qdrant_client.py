# vector_db/qdrant_client.py

from qdrant_client import AsyncQdrantClient

from config.settings import settings


# =========================================================
# PRIVATE SHARED QDRANT CLIENT
# =========================================================

_qdrant_client = AsyncQdrantClient(
    host = settings.QDRANT_HOST,
    port = settings.QDRANT_PORT
)


# QDrant Client Provider

async def get_qdrant_client() -> AsyncQdrantClient:
    """
    Dependency provider for shared async qdrant client instance.
    """
    
    return _qdrant_client