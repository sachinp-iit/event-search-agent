# dependencies/batch_ingestion_pipeline_dependency.py

from fastapi import Depends

from pipelines.batch_ingestion_pipeline import (
    BatchIngestionPipeline
)

from storage.transcript_loader import (
    TranscriptLoader
)

from utils.chunking import (
    TranscriptChunker
)

from utils.batch_processor import (
    BatchProcessor
)

from vector_db.vector_indexer import (
    VectorIndexer
)

from dependencies.transcript_loader_dependency import (
    transcript_loader_dependency
)

from dependencies.transcript_chunker_dependency import (
    transcript_chunker_dependency
)

from dependencies.batch_processor_dependency import (
    batch_processor_dependency
)

from dependencies.vector_indexer_dependency import (
    vector_indexer_dependency
)

from config.settings import settings

# =========================================================
# BATCH INGESTION PIPELINE DEPENDENCY
# =========================================================

async def batch_ingestion_pipeline_dependency (
    
    transcript_loader: TranscriptLoader = Depends (
        transcript_loader_dependency    
    ),
    
    transcript_chunker: TranscriptChunker = Depends (
        transcript_chunker_dependency
    ),
    
    batch_processor: BatchProcessor = Depends (
        batch_processor_dependency
    ),
    
    vector_indexer: VectorIndexer = Depends (
        vector_indexer_dependency
    )
) -> BatchIngestionPipeline:
       
    """
    Dependency provider for BatchIngestionPipeline.
    """
    
    return BatchIngestionPipeline (
        transcript_loader = transcript_loader,
        transcript_chunker = transcript_chunker,
        batch_processor = batch_processor,
        vector_indexer = vector_indexer
    )