# vector_db/qdrant_startup_manager.py

from vector_db.qdrant_collection_manager import (
    QdrantCollectionManager
)

from config.settings import settings


# =========================================================
# QDRANT STARTUP MANAGER
# =========================================================

class QdrantStartupManager:
    def __init__(
        self,
        collection_manager: QdrantCollectionManager
    ):
        
        self.collection_manager = collection_manager
        
    async def initialize(self) -> None:
        collection_exists = await (
            self.collection_manager.validate_collection()
        )
        
        if not collection_exists:
            
            await self.collection_manager.create_collection (
                vector_dimension = settings.EMBEDDING_DIMENSION
            )
            
        await self.collection_manager.get_collection_info()