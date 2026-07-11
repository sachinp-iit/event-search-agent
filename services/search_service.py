from agents.answer_generation_agent import AnswerGenerationAgent

from schemas.query_understanding_schema import (
    QueryUnderstandingSchema
)

from vector_db.semantic_query import (
    SemanticQueryEngine
)

# =========================================================
# SEARCH SERVICE
# =========================================================

class SearchService:

    def __init__(
        self,
        semantic_query_engine: SemanticQueryEngine,
        answer_generation_agent: AnswerGenerationAgent
    ) -> None:
        
        self.semantic_query_engine = semantic_query_engine
        self.answer_generation_agent = answer_generation_agent

    # =====================================================
    # SEMANTIC SEARCH
    # =====================================================

    async def search(
        self,
        user_query: str,
        query: QueryUnderstandingSchema
    ) -> str:
        """
        Executes semantic search using the
        structured query understanding schema.
        """

        search_results = await self.semantic_query_engine.semantic_search(
            query=query
        )

        transcript_chunks = [
            result["payload"]
            for result in search_results
        ]
        
        # Generation Response/Answer
        answer = await self.answer_generation_agent.generate_answer(
            user_query = user_query,
            transcript_chunks = transcript_chunks
        )

        return answer