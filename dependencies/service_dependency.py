# dependencies/service_dependency.py

from fastapi import Depends

from dependencies.answer_generation_dependency import get_answer_generation_agent

from dependencies.semantic_query_dependency import (
    semantic_query_dependency
)

from agents.answer_generation_agent import AnswerGenerationAgent

from services.search_service import SearchService

from vector_db.semantic_query import SemanticQueryEngine


# =========================================================
# SEARCH SERVICE DEPENDENCY
# =========================================================

def get_search_service(
    semantic_query_engine: SemanticQueryEngine = Depends (
        semantic_query_dependency
    ),
    
    answer_generation_agent: AnswerGenerationAgent = Depends (get_answer_generation_agent)
) -> SearchService:
    
    return SearchService(
        semantic_query_engine = semantic_query_engine,
        answer_generation_agent = answer_generation_agent
    )