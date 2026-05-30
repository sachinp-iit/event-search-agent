# vector_db/semantic_query.py

from qdrant_client import AsyncQdrantClient

from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue
)

from config.settings import settings

from langchain_core.embeddings import Embeddings


# =========================================================
# SEMANTIC QUERY ENGINE
# =========================================================

class SemanticQueryEngine:
    
    def __init__(self, qdrant_client: AsyncQdrantClient, embedding_model: Embeddings):
        
        self.qdrant_client = qdrant_client
        
        self.embedding_model = embedding_model
        
    
    # Semantic Search
    
    async def semantic_search (
        self, 
        query: str, 
        top_k: int | None = None,
        metadata_filters: dict | None = None
        ) -> list[dict]:
        
        """
        Semantic vector search against transcript collection.
        """
        
        # Query Embedding
        query_embedding = await self.embedding_model.aembed_query(query)
        
        # Optional Filters
        query_filters = None
        
        if metadata_filters:
            conditions = []
            
            for key, value in metadata_filters.items():
                conditions.append(
                    FieldCondition (
                        key = key, 
                        match = MatchValue(value = value)
                    )
                )
                
            query_filter = Filter (
                must = conditions
            )
            
        # Vector Search
        search_results = await self.qdrant_client.query_points (
            collection_name = settings.QDRANT_COLLECTION,
            query_vector = query_embedding,
            query_filter = query_filter,
            limit = top_k or settings.TOP_K_RESULTS,
            with_payload = True
        )
        
        # Normalized Response
        results = []
        
        for point in search_results.points:
            results.append (
                {
                    "id": point.id,
                    "score": point.score,
                    "payload": point.payload
                }
            )
            
        return results