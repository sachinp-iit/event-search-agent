# dependencies/ingestion_pipeline_dependency.py

from fastapi import Depends

from config.settings import settings

from pipelines.ingestion_pipeline import (
    IngestionPipeline
)

from storage.transcript_loader import (
    TranscriptLoader
)

from utils.chunking import (
    TranscriptChunker
)

from vector_db.vector_indexer import (
    VectorIndexer
)

from dependencies.vector_indexer_dependency import (
    vector_indexer_dependency
)

from dependencies.transcript_chunker_dependency import (
    transcript_chunker_dependency
)

from dependencies.transcript_loader_dependency import (
    transcript_loader_dependency
)


# =========================================================
# INGESTION PIPELINE DEPENDENCY
# =========================================================

async def ingestion_pipeline_dependency (
    
    transcript_loader: TranscriptLoader = Depends (
        transcript_loader_dependency    
    ),
    
    transcript_chunker: TranscriptChunker = Depends (
        transcript_chunker_dependency
    ),
    
    vector_indexer: VectorIndexer = Depends (
        vector_indexer_dependency
    )
) -> IngestionPipeline:
       
    return IngestionPipeline (
        transcript_loader = transcript_loader,
        transcript_chunker = transcript_chunker,
        vector_indexer = vector_indexer
    )
    