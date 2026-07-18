# Agent Source Documentation

------------------------------------------------------------------------

# Answer Generation Agent

``` python
# agents/answer_generation_agent.py

from langchain_core.language_models.chat_models import BaseChatModel

from prompts.prompt_manager import render_prompt


# =========================================================
# ANSWER GENERATION AGENT
# =========================================================
class AnswerGenerationAgent:
    """
    Generates the final grounded answer/response from the retrieved transcript chunks.
    """

    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
        
    # Generate Answer
    async def generate_answer(self, user_query: str, transcript_chunks: list[dict]) -> str:
        """
        Generate the final answer/response from retrieved transcript chunks
        """
        
        prompt = render_prompt(
            template_name = (
                "search_prompts"
                "semantic_search_prompt.jinja2"
            ),
            
            variables = {
                "user_query": user_query,
                "transcript_chunks": transcript_chunks
            }
        )
        
        response = await self.llm.ainvoke(prompt)
        
        return response.content
```

------------------------------------------------------------------------

# Query Understanding Agent

``` python
# agent/query_understanding_agent.py

from langchain_core.language_models.chat_models import BaseChatModel

from prompts.prompt_manager import render_prompt

from schemas.query_understanding_schema import QueryUnderstandingSchema

from typing import cast


# =========================================================
# QUERY UNDERSTANDING AGENT
# =========================================================
class QueryUnderstadingAgent:
    """
    Understanding the user's query and converts it into
    structured metadata for downstream retrieval.
    """
    
    def __init__(self, llm: BaseChatModel):        
        self.llm = llm
        
        # Structured output LLM
        self.structured_llm = (
            self.llm.with_structured_output(QueryUnderstandingSchema)
        )
        
    # Analyze Query
    async def analyze_query(
        self, 
        user_query: str,
        conversation_history: list[dict] | None = None,
        conversation_summary: str | None = None
        ) -> QueryUnderstandingSchema:
        """
        Analyze a user query and return a structured representation.
        """        
        
        # Load Prompt
        prompt = render_prompt (
            template_name = (
                "agents/"
                "query_understanding_prompt.jinja2"
                ),
            variables = {
                "user_query": user_query,
                "conversation_history":
                    conversation_history or [],
                "conversation_summary": conversation_summary or "",
                },
        )
        
        # LLM
        response = await self.structured_llm.ainvoke(prompt)

        # Return        
        # return cast(QueryUnderstandingSchema, response)
        return QueryUnderstandingSchema.model_validate(response)
```

------------------------------------------------------------------------

# Retrieval Agent

``` python
# agents/retrieval_agent.py

from services.search_service import SearchService

from schemas.query_understanding_schema import QueryUnderstandingSchema


# =========================================================
# RETRIEVAL AGENT
# =========================================================

class RetrievalAgent:
    """
    Retrieves relevant transcript chunks based on the structured query.
    """
    
    def __init__(self, search_service: SearchService) -> None:
        self.search_service = search_service
        
    # Retrieve
    async def retrieve(self, query: QueryUnderstandingSchema) -> list[dict]:
        """
        Retrieve relevant transcript chunks
        """
        
        search_results = await self.search_service.semantic_search(user_query=query.normalized_query)
        
        return search_results
        
    
```

------------------------------------------------------------------------

# State

``` python
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
```

------------------------------------------------------------------------

# Entity Extraction Agent

``` python
# agents/knowledge_graph/entity_extraction_agent.py

from langchain_core.language_models.chat_models import BaseChatModel

from prompts.prompt_manager import render_prompt

from schemas.knowledge_graph_schema import KnowledgeGraphSchema


# =========================================================
# ENTITY EXTRACTION AGENT
# =========================================================

class EntityExtractionAgent:
    """
    Extract entities and relationship from a conversation summary.
    """
    
    def __init__(self, llm: BaseChatModel):
        self.structured_llm = (
            llm.with_structured_output(KnowledgeGraphSchema)
        )
        
        
    async def extract(self, conversation_summary: str) -> KnowledgeGraphSchema:
        """
        Extract entities and relationships.
        """
        prompt = render_prompt(
            template_name=(
                "agents/"
                "knowledge_graph_prompt.jinja2"
            ),
            variables={
                "conversation_summary": conversation_summary
            }
        )
        
        response = await self.structured_llm.ainvoke(prompt)
        
        return KnowledgeGraphSchema.model_validate(response)
        
    
```
