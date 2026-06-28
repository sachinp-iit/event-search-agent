# schemas/query_understanding_schema.py

from pydantic import BaseModel

from pydantic import Field


# =========================================================
# QUERY UNDERSTANDING SCHEMA
# =========================================================

class QueryUnderstandingSchema(BaseModel):
    """
    Structured representation of the user's query.
    
    Produced by the Query Understanding Agent and
    consumed by the Retrieval Agent.
    """
    
    # User Query
    original_query: str = Field(description="Original user query.")    
    normalized_query: str = Field(description="Normalized query for retrieval.")
    
    # User Intent
    intent: str = Field(
        description=(
            "Primary user intent. "
            "Examples: search, summarize, compare, "
            "recommend, analytics."
        )
    )
    
    # Event Filters
    event_name: str | None = Field(default=None, description="Event name filter.")
    event_topic: str | None = Field(default=None, description="Event topic filter.")
    speaker_name: str | None = Field(default=None, description="Speaker name filter.")
    company_name: str | None = Field(default=None, description="Company name filter.")
    domain: str | None = Field(default=None, description="Domain name filter.")
    category: str | None = Field(default=None, description="Category name filter.")
    event_location: str | None = Field(default=None, description="Location filter.")
    
    # Date Filters
    event_start_date: str | None = Field(default=None, description="Start date filter")
    event_end_date: str | None = Field(default=None, description="End date filter")
    
    # Search Options
    top_k: int = Field(default = 10, description="Maximum search results.")
    use_hybrid_search: bool = Field(default=True, description="Use keyword + vector search.")
    use_reranker: bool = Field(default=True, description="Enable reranking.")
    
    # Query Expansion
    expanded_queries: list[str] = Field(default_factory=list, description="Alternative search queries.")
    
    # Reasoning
    reasoning: str = Field(description="Reasoning behind extracted intent and filters.")