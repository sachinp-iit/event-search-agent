# vector_db/vector_indexer.py

import uuid

from qdrant_client import AsyncQdrantClient

from qdrant_client.models import PointStruct

from config.settings import settings

from langchain_core.embeddings import Embeddings


# =========================================================
# VECTOR INDEXER
# =========================================================

class VectorIndexer:
    
    def __init__(self, qdrant_client: AsyncQdrantClient, embedding_model: Embeddings):
        
        self.qdrant_client = qdrant_client
        
        self.embedding_model = embedding_model
        
        self.batch_size = settings.INGESTION_BATCH_SIZE
        
    # --------------------------------------------------------------------------------------------
    
    # Index transcript chunks
    
    async def index_transcript_chunks(self, transcript_chunks: list[dict]) -> None:
        """
        Generates embeddings and stores transcript chunks into Qdrant.
        """
        
        # Check if there are is a data in chunks
        if not transcript_chunks:
            return
        
        for start_index in range(0, len(transcript_chunks), self.batch_size):
            
            batch = transcript_chunks[
                start_index: start_index + self.batch_size
            ]
            
            await self._process_batch(transcript_chunks=batch)
            
    
    # PROCESS BATCH
    async def _process_batch(self, transcript_chunks: list[dict]) -> None:
        
        transcript_texts = [
            chunk["transcript_text"]
            for chunk in transcript_chunks   
        ]
        
        embeddings = await (self.embedding_model.aembed_documents(transcript_texts))
        
        points = []
        
        for chunk, embedding in zip (transcript_chunks, embeddings):
            
            point = PointStruct (
                id = self._generate_point_id
                (
                    chunk = chunk
                ),       
                vector = embedding,
                payload = self._build_payload(chunk = chunk)
                )

            points.append(point)
                
        
        await self._upsert_points(points = points)
        
    
    # UPSERT POINTS
    async def _upsert_points(self, points: list[PointStruct]) -> None:
        
        await self.qdrant_client.upsert(
            collection_name = settings.QDRANT_COLLECTION,
            points = points,
            wait = True
        )
        
        
    # PAYLOAD BUILDER
    def _build_payload(self, chunk: dict) -> dict:
        
        return {
            
            "event_name": 
                chunk.get("event_name"),
                
            "event_topic":
                chunk.get("event_topic"),
                
            "speaker_name":
                chunk.get("speaker_name"),
                
            "event_date":
                chunk.get("event_date"),
                
            "event_company":
                chunk.get("event_company"),
                
            "event_location":
                chunk.get("event_location"),
                
            "domain":
                chunk.get("domain"),
                
            "category":
                chunk.get("category"),
                
            "file_name":
                chunk.get("file_name"),
                
            "transcript_text":
                chunk.get("transcript_text")
        }
        

    # IDEMPOTENT POINT ID
    def _generate_point_id(self, chunk: dict) -> str:
        
        seed = (
            f"{chunk.get('file_name', '')}"
            f"{chunk.get('event_name', '')}"
            f"{chunk.get('transcript_text', '')}"
        )
        
        return str (
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                seed
            )
        )