# api/routes/search_routes.py

from fastapi import APIRouter

from fastapi import Depends

from services.search_service import SearchService

from dependencies.service_dependency import get_search_service

from schemas.search_schema import SearchRequest

from schemas.search_schema import SearchResponse

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
):
    
    # TODO: Replace Mock Transcript with Real Transcript in later stage
    # Temporary Mock Transcript Data
    
    transcript_chunks = [
        {
            "event_name": "AI Summit 2026",
            "event_topic": "Agentic AI System",
            "speaker_name": "John Doe",
            "event_date": "2026-05-24",
            "transcript_text": (
                "Agentic AI systems can orchestrate"
                "multi-step reasoning workflows."
            )
        }
    ]
    
    
    # Generate Response
    
    response = search_service.generate_semantic_search_response(
        user_query = request.user_query,
        transcript_chunks = transcript_chunks
    )
    
    return {
        "user_query": request.user_query,
        "response": response
    }