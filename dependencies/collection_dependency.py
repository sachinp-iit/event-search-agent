# dependency/collection_dependency.py

from fastapi import Depends

from qdrant_client import AsyncQdrantClient

from dependencies.qdrant_dependency import qdrant_client_dependency

from vector_db.collection_manager import CollectionManager


# =========================================================
# COLLECTION MANAGER DEPENDENCY
# =========================================================

async def collection_manager_depedency(
    qdrant_client: AsyncQdrantClient = Depends(
        qdrant_client_dependency
    )
) -> CollectionManager:
    
    """
    Dependency injection provider for CollectionManager
    """
    
    return CollectionManager(
        qdrant_client = qdrant_client
    )