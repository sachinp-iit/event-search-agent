# core/container.py

from database.sql_server_client import get_db_session

from vector_db.qdrant_client import get_qdrant_client

from models.embedding.embedding_loader import get_embedding_model

from models.llm.openrouter_client import llm

from storage.metadata_loader import MetadataLoader

from storage.transcript_loader import TranscriptLoader

from utils.chunking import TranscriptChunker

from utils.batch_processor import BatchProcessor

from vector_db.qdrant_collection_manager import QdrantCollectionManager

from vector_db.vector_indexer import VectorIndexer

from vector_db.semantic_query import SemanticQueryEngine

from services.metadata_enrichment_service import MetadataEnrichmentService

from services.search_service import SearchService

from services.ingestion_service import IngestionService

from pipelines.batch_ingestion_pipeline import BatchIngestionPipeline

from config.settings import settings


# =========================================================
# APPLICATION CONTAINER
# =========================================================
class ApplicationContainer:
    """
    Application composition root. Responsible for constructing and wiring all dependencies.
    """
    
    def __init__(self):
        self._initialized = False

        
    # Object Initializer
    async def initialize(self):
        if self._initialized:
            return
        
        # Initialize Core Components
        self.db_session = await anext(get_db_session())
        
        self.qdrant_client = await (get_qdrant_client())
        
        self.embedding_model = await (get_embedding_model())
        
        self.llm = llm
        
        # Initialize Storage
        self.metadata_loader = MetadataLoader(self.db_session)
        
        self.transcript_loader = TranscriptLoader(settings.RAW_TRANSCRIPTS_DIRECTORY)
        
        # Initialize Utilities
        self.chunker = TranscriptChunker()
        
        self.batch_processor = BatchProcessor (
            batch_size = settings.INGESTION_BATCH_SIZE,
            max_concurrency = settings.MAX_CONCURRENT_BATCHES
        )
        
        # Initialize Vector DB
        self.collection_manager = (
            QdrantCollectionManager (self.qdrant_client)
        )
        
        self.vector_indexer = VectorIndexer(self.qdrant_client, self.embedding_model)
        
        self.semantic_query = (SemanticQueryEngine (self.qdrant_client, self.embedding_model))
        
        # Initialize Services
        self.metadata_service = MetadataEnrichmentService(self.metadata_loader)
        
        self.search_service = SearchService(self.llm, self.semantic_query)
        
        # Initialize Ingestion Pipeline
        self.ingestion_pipeline = (BatchIngestionPipeline (
            self.transcript_loader,
            self.metadata_service,
            self.chunker,
            self.batch_processor,
            self.vector_indexer
            
        ))
        
        self.ingestion_service = (IngestionService(
            self.metadata_loader,
            self.ingestion_pipeline
        ))
        
        self._initialized = True
        

# Singleton Container
container = ApplicationContainer()