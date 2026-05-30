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
        
    # --------------------------------------------------------------------------------------------
    
    # Index transcript chunks
    
    async def index_transcript_chunks(self, transcript_chunks: list[dict]) -> None:
        """
        Generates embeddings and stores transcript chunks into Qdrant.
        """
        
        # Prepare Texts
        
        transcript_texts = [
            chunk["transcript_texts"]
            for chunk in transcript_chunks
        ]
        
        
        # Generate Embeddings
        
        embeddings = await self.embedding_model.aembed_documents (
            transcript_texts
        )
        
        # Build Qdrant Points
        
        points = []
        
        for chunk, embedding in zip(transcript_chunks, embeddings):

            point = PointStruct(
                id = str(uuid.uuid4()),
                vector = embedding,
                payload = {
                    "event_name": chunk.get("event_name"),
                    "event_topic": chunk.get("event_topic"),
                    "speaker_name": chunk.get("speaker_name"),
                    "event_date": chunk.get("event_date"),
                    "transcript_text": chunk.get("transcript_text")
                }
            )
            
            points.append(point)
            
        # Upsert into Qdrant
        
        await self.qdrant_client.upsert (
            collection_name = settings.QDRANT_COLLECTION,
            points = points
        )