# api/routes/search_routes.py

from fastapi import APIRouter

from fastapi import Depends

from agents.query_understanding_agent import QueryUnderstadingAgent

from dependencies.query_understanding_dependency import get_query_understanding_agent

from dependencies.service_dependency import get_search_service

from dependencies.memory_prompt_helper_dependency import get_memory_prompt_helper

from memory.memory_manager import MemoryManager

from memory.memory_prompt_helper import MemoryPromptHelper

from dependencies.memory_dependency import get_memory_manager

from schemas.search_schema import (
    SearchRequest,
    SearchResponse
)

from services.search_service import SearchService

from services.conversation_service import ConversationService

from dependencies.conversation_service_dependency import get_conversation_service

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
    "/search",
    response_model = SearchResponse
    )

async def semantic_search(
    request: SearchRequest,
    query_understanding_agent: QueryUnderstadingAgent = Depends (
        get_query_understanding_agent
    ),
    search_service: SearchService = Depends (
        get_search_service
    ),
    memory_manager: MemoryManager = Depends (
        get_memory_manager
    ),
    memory_prompt_helper: MemoryPromptHelper = Depends(
        get_memory_prompt_helper
    ),
    conversation_service: ConversationService = Depends (
        get_conversation_service
    )
) -> SearchResponse:
    """
    Semantic transcript search endpoint
    """
    
    # Load Conversation Memory
    memory = memory_manager.get_memory(request.session_id)
    
    conversation_history = memory_prompt_helper.build_context(memory)
    
    conversation_summary = await conversation_service.summarize_conversation(memory)
    
    # Understanding Query
    query = await query_understanding_agent.analyze_query(
        user_query = request.user_query,
        conversation_history = conversation_history,
        conversation_summary = conversation_summary
    )
    
    # Execute Search
    response = await search_service.search(
        user_query = request.user_query,
        query = query
    )
    
    # Update Memory
    memory.add_message(role="user", content = request.user_query)
    memory.add_message(role="assistant", content = response)
    
    return SearchResponse(
        session_id = request.session_id,
        user_query=request.user_query,
        response = response
    )