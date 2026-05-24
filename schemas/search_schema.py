# schemas/search_schema.py

from pydantic import BaseModel

from pydantic import Field


# =========================================================
# SEARCH REQUEST SCHEMA
# =========================================================

class SearchRequest(BaseModel):
    
    user_query: str = Field(
        ...,
        description="Natural language search query"
    )
    

# =========================================================
# SEARCH RESPONSE SCHEMA
# =========================================================

class SearchResponse(BaseModel):
    
    user_query: str
    
    response: str