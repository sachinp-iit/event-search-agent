# services/search_service.py

from vector_db.semantic_query import SemanticQueryEngine

from prompts.prompt_manager import render_prompt

from langchain_core.language_models.chat_models import BaseChatModel


# =========================================================
# SEARCH SERVICE
# =========================================================

class SearchService:
    
    def __init__(
        self, 
        llm: BaseChatModel, 
        semantic_query_engine: SemanticQueryEngine
        ):
            self.llm = llm
            self.semantic_query_engine = semantic_query_engine
            
    
    # Semantic Search
    
    async def semantic_search(
        self,
        user_query: str
    ) -> str:
        
        # Retrieve relevant transcripts
        search_results = await self.semantic_query_engine.semantic_search (
            query = user_query
        )
        
        # Extract Payloads
        
        transcript_chunks = [
            result["payload"]
            for result in search_results
        ]
        
        # Render Prompt
        final_prompt = render_prompt (
            template_name = "search_prompts/semantic_search_prompt.jinja2",
            
            variables = {
                "user_query": user_query,
                "transcript_chunks": transcript_chunks
            }
        )
        
        
        # LLM Invocation
        response = await self.llm.ainvoke (
            final_prompt
        )
        
        return response.content