# dependencies/service_dependency.py

from fastapi import Depends

from dependencies.llm_dependency import get_llm

from services.search_service import SearchService


# =========================================================
# SEARCH SERVICE DEPENDENCY
# =========================================================

def get_search_service(
    llm = Depends(get_llm)
) -> SearchService:
    
    """
    Provides SearchService instance with injected LLM dependency.
    """
    
    return SearchService(llm = llm)