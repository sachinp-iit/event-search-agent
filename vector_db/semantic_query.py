# vector_db/semantic_query.py

from qdrant_client import AsyncQdrantClient

from qdrant_client.models import (
    Condition,
    FieldCondition,
    Filter,
    MatchValue
)

from config.settings import settings

from langchain_core.embeddings import Embeddings

from schemas.query_understanding_schema import QueryUnderstandingSchema


# =========================================================
# SEMANTIC QUERY ENGINE
# =========================================================

class SemanticQueryEngine:
    
    def __init__(self, qdrant_client: AsyncQdrantClient, embedding_model: Embeddings) -> None:
        
        self.qdrant_client = qdrant_client        
        self.embedding_model = embedding_model
        
    
    # Semantic Search    
    async def semantic_search (self, query: QueryUnderstandingSchema) -> list[dict]:
        
        """
        Semantic vector search against transcript collection.
        """
        
        # Query Embedding
        query_embedding = await self.embedding_model.aembed_query(query.normalized_query)
        
        # Metadata Filters
        conditions: list[Condition] = []
        
        filter_mapping = {
            "event_name": query.event_name,
            "event_topic": query.event_topic,
            "speaker_name": query.speaker_name,
            "event_company": query.company_name,
            "domain": query.domain,
            "category": query.category,
            "event_location": query.event_location
        }
        
        for key, value in filter_mapping.items():
            
            if value is not None:
                conditions.append(FieldCondition(key = key, match = MatchValue(value = value)))
                
                
        query_filter = None
        
        if conditions:
            query_filter = Filter(must = conditions)
            
        # Vector Search
        search_results = await self.qdrant_client.query_points(
            collection_name = settings.QDRANT_COLLECTION,
            query = query_embedding,
            query_filter = query_filter,
            limit = query.top_k,
            with_payload = True
        )
        
        # Normalize Results
        results: list[dict] = []
        
        for point in search_results.points:
            results.append(
                {
                    "id": point.id,
                    "score": point.score,
                    "payload": point.payload
                }
            )
            
        return results