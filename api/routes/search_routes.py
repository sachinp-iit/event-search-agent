# api/routes/search_routes.py

from fastapi import APIRouter

from fastapi import Depends

from services.search_service import SearchService

from dependencies.service_dependency import get_search_service

from schemas.search_schema import (
    SearchRequest,
    SearchResponse
)


# ================================================
# API ROUTER INITIALIZATION
# ================================================

router = APIRouter(
    prefix = "/search",
    tags = ["Semantic Search"]
)


# ================================================
# SEMANTIC SEARCH ENDPOINT
# ================================================

@router.post(
    "/",
    response_model = SearchResponse
    )

async def semantic_search(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service)
) -> SearchResponse:
    
    response = await search_service.semantic_search (
        user_query = request.user_query
    )
    
    return SearchResponse (
        user_query = request.user_query,
        response = response
    )