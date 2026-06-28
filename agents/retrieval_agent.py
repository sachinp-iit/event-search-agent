# agents/retrieval_agent.py

from services.search_service import SearchService

from schemas.query_understanding_schema import QueryUnderstandingSchema


# =========================================================
# RETRIEVAL AGENT
# =========================================================

class RetrievalAgent:
    """
    Retrieves relevant transcript chunks based on the structured query.
    """
    
    def __init__(self, search_service: SearchService) -> None:
        self.search_service = search_service
        
    # Retrieve
    async def retrieve(self, query: QueryUnderstandingSchema) -> list[dict]:
        """
        Retrieve relevant transcript chunks
        """
        
        search_results = await self.search_service.semantic_search(user_query=query.normalized_query)
        
        return search_results
        
    