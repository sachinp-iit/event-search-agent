# agents/state.py

from typing import Annotated

from typing import Any

from typing import TypedDict

from langgraph.graph.message import add_messages


# =========================================================
# AGENT STATE
# =========================================================
class AgentState(TypedDict):
    """
    Shared state passed across all Langgraph agents.
    - Maintain conversation context
    - Share intermediate outputs
    - Control workflow execution
    """
    
    # User Input
    user_query: str
    normalized_query: str
    intent: str
    domain: str | None
    category: str | None
    
    # Filters
    metadata_filters: dict[str, Any]
    
    # Retrieval
    retrieved_chunks: list[dict]
    reranked_chunks: list[dict]
    recommendations: list[dict]
    
    # Summarization
    summary: str
    
    # Response
    final_response: str
    
    # Observability
    execution_trace: list[str]
    errors: list[str]
    
    # Chat History
    messages: Annotated[list, add_messages]