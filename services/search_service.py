# services/search_service.py

from langchain_core.language_models.chat_models import BaseChatModel

from prompts.prompt_manager import render_prompt


# =========================================================
# SEARCH SERVICE
# =========================================================

class SearchService:
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        
    # GENERATE SEMANTIC SEARCH RESPONSE
    def generate_semantic_search_response(
        self, user_query: str,
        transcript_chunks: list
    ):
        
        # RENDER PROMPT TEMPLATE
        final_prompt = render_prompt(
            template_name = "search_prompts/semantic_search_prompt.jinja2",
            
            variables = {
                "user_query": user_query,
                "transcript_chunks": transcript_chunks
            }
        )
        
        # LLM Invocation
        response = self.llm.invoke(final_prompt)
        
        # Return Response
        return response.content