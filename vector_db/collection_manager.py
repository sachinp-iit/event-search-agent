# vector_db/collection_manager.py

from qdrant_client import AsyncQdrantClient

from qdrant_client.models import Distance
from qdrant_client.models import VectorParams

from config.settings import settings


# =========================================================
# COLLECTION MANAGER
# =========================================================

class CollectionManager:
    
    def __init__(self, qdrant_client: AsyncQdrantClient):
        self.qdrant_client = qdrant_client
        
    
    # Create Collection
    async def create_collection(self, vector_dimension: int) -> None:
        """
        Creates transcript vector collection if it does not already exist.
        """
        
        # Check existing collection
        collection_response = await self.qdrant_client.get_collections()
        existing_collections = [
            collection.name
            for collection in collection_response.collections
        ]
        
        # Skip if collection exists
        if settings.QDRANT_COLLECTION in existing_collections:
            return
        
        # Create vector collection
        await self.qdrant_client.create_collection(
            collection_name = settings.QDRANT_COLLECTION,
            
            vectors_config = VectorParams(
                size = vector_dimension,
                distance = Distance.COSINE
            )
        )