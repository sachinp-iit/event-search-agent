# dependencies/qdrant_startup_manager_dependency.py

from fastapi import Depends

from vector_db.qdrant_startup_manager import (
    QdrantStartupManager
)

from vector_db.qdrant_collection_manager import (
    QdrantCollectionManager
)

from dependencies.qdrant_collection_manager_depedency import (
    qdrant_collection_manager_depedency
)


# ================================================
# QDRANT STARTUP MANAGER DEPENDENCY
# ================================================

async def qdrant_startup_manager_dependency (
    
    collection_manager: QdrantCollectionManager = Depends (
        qdrant_collection_manager_depedency
    )
) -> QdrantStartupManager:
    
    return QdrantStartupManager (
        collection_manager = collection_manager
    )

