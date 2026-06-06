# pipelines/batch_ingestion_pipeline.py

from storage.transcript_loader import (
    TranscriptLoader
)

from utils.chunking import (
    TranscriptChunker
)

from vector_db.vector_indexer import (
    VectorIndexer
)

from utils.batch_processor import (
    BatchProcessor
)

from schemas.transcript_chunk_schema import (
    TranscriptChunkSchema
)


# =========================================================
# BATCH INGESTION PIPELINE
# =========================================================

class BatchIngestionPipeline:
    """
    Production grade ingestion pipeline.
    - Load transcripts
    - Chunk transcripts
    - Validate chunks
    - Batch processing
    - Concurrent indexing
    """
        
    def __init__(
        self, 
        transcript_loader: TranscriptLoader,
        transcript_chunker: TranscriptChunker,
        batch_processor: BatchProcessor,
        vector_indexer: VectorIndexer
    ):
        
        # Dependencies
        self.transcript_loader = transcript_loader
        self.transcript_chunker = transcript_chunker
        self.batch_processor = batch_processor
        self.vector_indexer = vector_indexer
        
    
    # Ingest all transcripts
    async def ingest_all_transcripts (self) -> None:
        # Load Transcripts
        transcripts = await (self.transcript_loader.load_all_transcripts())
        
        # Chunk Transcripts
        transcript_chunks = await (self.transcript_chunker.chunk_transcripts(transcripts = transcripts))
        
        # Validate Chunks
        validated_chunks = [
            TranscriptChunkSchema(**chunk).model_dump()
            for chunk in transcript_chunks
        ]
        
        # Process in batches
        await self.batch_processor.process_batches(
            items = validated_chunks,
            processor = self._index_batch
        )
        

    # Process in Batches
    async def _index_batch(self, batch: list[dict]) -> None:
        
        # Index Chunks
        await self.vector_indexer.index_transcript_chunks(
            transcript_chunks = batch
        )