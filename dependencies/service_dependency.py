# dependencies/service_dependency.py

from fastapi import Depends

from dependencies.llm_dependency import get_llm

from dependencies.semantic_query_dependency import (
    semantic_query_dependency
)

from services.search_service import SearchService

from vector_db.semantic_query import SemanticQueryEngine

from langchain_core.language_models.chat_models import (
    BaseChatModel
)

# =========================================================
# SEARCH SERVICE DEPENDENCY
# =========================================================

def get_search_service(
    llm: BaseChatModel = Depends ( 
        get_llm 
    ),
    
    semantic_query_engine: SemanticQueryEngine = Depends (
        semantic_query_dependency
    )
) -> SearchService:
    
    return SearchService (
        llm = llm,
        semantic_query_engine = semantic_query_engine
    )