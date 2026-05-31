# vector_db/qdrant_collection_manager.py

from qdrant_client import AsyncQdrantClient

from qdrant_client.models import Distance
from qdrant_client.models import VectorParams

from qdrant_client.models import HnswConfigDiff
from qdrant_client.models import OptimizersConfigDiff
from qdrant_client.models import ScalarQuantization
from qdrant_client.models import ScalarQuantizationConfig
from qdrant_client.models import ScalarType

from qdrant_client.models import PayloadSchemaType

from config.settings import settings


# =========================================================
# QDRANT COLLECTION MANAGER
# =========================================================

class QdrantCollectionManager:
    
    def __init__(self, qdrant_client: AsyncQdrantClient):
        self.qdrant_client = qdrant_client
        
    
    # Create Collection
    async def create_collection(self, vector_dimension: int) -> None:
        """
        Creates transcript vector collection if it does not already exist.
        """
        
        # Check existing collection
        collection_exists = await self.qdrant_client.collection_exists(
            collection_name = settings.QDRANT_COLLECTION
        )
        
        if collection_exists:
            return
        
        await self.qdrant_client.create_collection (
            collection_name = settings.QDRANT_COLLECTION,
            
            vectors_config = VectorParams (
                size = vector_dimension,
                distance = Distance.COSINE
            ),
            
            hnsw_config = HnswConfigDiff (
                m = 32, # Each vector can connect to upto 32 neighboring vectors
                ef_construct = 200 # Effort spend by vector database for creating the graph 
            ),
            
            optimizers_config = OptimizersConfigDiff (
                indexing_threshold = 10000
            ),
            
            quantization_config = ScalarQuantization (
                scalar = ScalarQuantizationConfig (
                    type = ScalarType.INT8,
                    always_ram = True
                )
            )
        )
        
        await self._create_payload_indexes()
        
    
    # Payload Indexes
    async def _create_payload_indexes(self) -> None:
        indexed_fields = [
            settings.EVENT_NAME,
            settings.EVENT_TOPIC,
            settings.SPEAKER_NAME,
            settings.EVENT_DATE,
            settings.EVENT_COMPANY,
            settings.EVENT_LOCATION,
            settings.DOMAIN,
            settings.CATEGORY
        ]
        
        for field in indexed_fields:
            await self.qdrant_client.create_payload_index (
                collection_name = settings.QDRANT_COLLECTION,
                field_name = field,
                field_schema = PayloadSchemaType.KEYWORD
            )
            
            
    # Collection Info
    async def get_collection_info(self):
        
        return await self.qdrant_client.get_collection (
            collection_name = settings.QDRANT_COLLECTION
        )
        
    
    # Validate Collection
    async def validate_collection(self) -> bool:
        
        return await self.qdrant_client.collection_exists (
            collection_name = settings.QDRANT_COLLECTION
        )