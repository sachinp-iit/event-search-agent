# scripts/ingest_transcripts.py

import asyncio

from config.settings import settings

from vector_db.qdrant_client import get_qdrant_client

from vector_db.qdrant_collection_manager import QdrantCollectionManager

from vector_db.qdrant_startup_manager import QdrantStartupManager

from models.embedding.embedding_loader import get_embedding_model

from vector_db.vector_indexer import VectorIndexer

from storage.transcript_loader import TranscriptLoader

from utils.chunking import TranscriptChunker

from utils.batch_processor import BatchProcessor

from pipelines.batch_ingestion_pipeline import BatchIngestionPipeline

# =========================================================
# INGESTION ENTRYPOINT
# =========================================================

async def main() -> None:
    
    # QDrant Client
    qdrant_client = await get_qdrant_client()
    
    # Collection Initialization
    collection_manager = QdrantCollectionManager(qdrant_client = qdrant_client)
    
    startup_manager = QdrantStartupManager(collection_manager = collection_manager)
    
    await startup_manager.initialize()
    
    # Embedding Model
    embedding_model = await (get_embedding_model())
    
    # Vector Indexer
    vector_indexer = VectorIndexer (qdrant_client = qdrant_client, embedding_model = embedding_model)
    
    # Transcript Loader
    transcript_loader = TranscriptLoader(transcript_directory = settings.RAW_TRANSCRIPTS_DIRECTORY)
    
    # Transcript Chunker
    transcript_chunker = TranscriptChunker()
    
    # Batch Processor
    batch_processor = BatchProcessor(
        batch_size = settings.INGESTION_BATCH_SIZE,
        max_concurrency = settings.MAX_CONCURRENT_BATCHES
        )
    
    # Ingestion Pipeline
    ingestion_pipeline = (
        BatchIngestionPipeline(
            transcript_loader = transcript_loader,
            transcript_chunker = transcript_chunker,
            batch_processor = batch_processor,
            vector_indexer = vector_indexer
        )
    )
    
    # Start Ingestion
    await (ingestion_pipeline.ingest_all_transcripts())
    
    print("Transcription ingestion completed successfully.")
    
    await qdrant_client.close()
    

# Script Entrypoint
if __name__ == "__main__":
    asyncio.run(main())
    

# =========================================================
# EXECUTION COMMAND
# =========================================================
# from command prompt you execute following command to ingest 
# all your transcripts from a "raw_transcripts" folder.
# python scripts/ingest_transcripts.py