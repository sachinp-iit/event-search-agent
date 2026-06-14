# pipelines/batch_ingestion_pipeline.py

from storage.transcript_loader import (
    TranscriptLoader
)

from services.metadata_enrichment_service import MetadataEnrichmentService

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
        metadata_enrichment_service: MetadataEnrichmentService,
        transcript_chunker: TranscriptChunker,
        batch_processor: BatchProcessor,
        vector_indexer: VectorIndexer
    ):
        
        # Dependencies
        self.transcript_loader = transcript_loader
        self.metadata_enrichment_service = metadata_enrichment_service
        self.transcript_chunker = transcript_chunker
        self.batch_processor = batch_processor
        self.vector_indexer = vector_indexer
        
    
    # Ingest Single Event
    async def ingest_event(self, event_id: int, transcript_file_name: str) -> None:
        
        # Load Transcript
        transcript = await (
            self.transcript_loader.load_transcript(
                transcript_file_name
            )
        )
        
        # Chunk Transcript
        chunks = await (self.transcript_chunker.chunk_transcript(
            transcript
        ))
        
        # Build Chunk Objects
        transcript_chunks = [
            {
                "chunk_sequence": index,
                "transcript_text": chunk
            }
            
            for index, chunk in enumerate(chunks)
        ]
        
        # Enrich with SQL Metadata
        enriched_chunks = await (
            self.metadata_enrichment_service
            .enrich_chunks(
                chunks = transcript_chunks,
                event_id = event_id
            )
        )
        
        # Validate Chunks
        validated_chunks = [
            TranscriptChunkSchema(**chunk).model_dump()
            for chunk in enriched_chunks
        ]
        
        # Indexed Enriched Chunks in Batches
        await self.batch_processor.process_batches(
            items = validated_chunks,
            processor = self.vector_indexer.index_transcript_chunks
        )