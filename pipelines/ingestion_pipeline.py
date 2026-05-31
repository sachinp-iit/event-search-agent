# pipelines/ingestion_pipeline.py

from storage.transcript_loader import (
    TranscriptLoader
)

from utils.chunking import (
    TranscriptChunker
)

from vector_db.vector_indexer import (
    VectorIndexer
)


# =========================================================
# INGESTION PIPELINE
# =========================================================

class IngestionPipeline:
    
    def __init__(
        self, 
        transcript_loader: TranscriptLoader,
        transcript_chunker: TranscriptChunker,
        vector_indexer: VectorIndexer
    ):
        
        self.transcript_loader = transcript_loader
        self.transcript_chunker = transcript_chunker
        self.vector_indexer = vector_indexer
        
    
    # Ingest all transcripts
    async def ingest_all_transcripts (self) -> None:
        # Load Transcripts
        transcripts = await (self.transcript_loader.load_all_transcripts())
        
        # Chunk Transcripts
        transcript_chunks = await (self.transcript_chunker.chunk_transcripts(transcripts = transcripts))
        
        # Index Chunks
        await self.vector_indexer.index_transcript_chunks(transcript_chunks = transcript_chunks)