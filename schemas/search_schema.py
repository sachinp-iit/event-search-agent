# schemas/search_schema.py

from pydantic import BaseModel

from pydantic import Field


# =========================================================
# SEARCH REQUEST SCHEMA
# =========================================================

class SearchRequest(BaseModel):
    """
    Semantic search request.
    """
    
    session_id: str = Field(
        description = "Unique conversation session id."
    )
    
    user_query: str = Field(
        ...,
        description="Natural language search query"
    )
    

# =========================================================
# SEARCH RESPONSE SCHEMA
# =========================================================

class SearchResponse(BaseModel):
    
    session_id: str
    
    user_query: str
    
    response: str