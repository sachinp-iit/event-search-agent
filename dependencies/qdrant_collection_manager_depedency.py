# dependency/qdrant_collection_dependency.py

from fastapi import Depends

from qdrant_client import AsyncQdrantClient

from dependencies.qdrant_dependency import qdrant_client_dependency

from vector_db.qdrant_collection_manager import QdrantCollectionManager


# =========================================================
# QDRANT COLLECTION MANAGER DEPENDENCY
# =========================================================

async def qdrant_collection_manager_depedency(
    qdrant_client: AsyncQdrantClient = Depends(
        qdrant_client_dependency
    )
) -> QdrantCollectionManager:
    
    """
    Dependency injection provider for QDrantCollectionManager
    """
    
    return QdrantCollectionManager(
        qdrant_client = qdrant_client
    )