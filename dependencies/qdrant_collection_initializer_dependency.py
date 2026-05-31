# dependencies/qdrant_collection_initializer_dependency.py

from fastapi import Depends

from vector_db.qdrant_collection_manager import (
    QdrantCollectionManager
)

from dependencies.qdrant_collection_manager_depedency import (
    qdrant_collection_manager_depedency
)

from config.settings import settings


# =========================================================
# QDRANT COLLECTION INITIALIZER
# =========================================================

async def initialize_qdrant_collection (
    
    collection_manager: QdrantCollectionManager = Depends (
        qdrant_collection_manager_depedency
    )
) -> None:
    """
    Startup initilization
    - Collection Creation
    - Collection Validation
    - HNSW Validation
    - Payload Index Validation
    - Quantization Validation
    """
    
    collection_exists = await (
        collection_manager.validate_collection()
    )
    
    if collection_exists:
        return
    
    await collection_manager.create_collection (
        vector_dimension = settings.EMBEDDING_DIMENSION
    )