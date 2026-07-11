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
        conversation_history: list[dict] | None = None
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
                    conversation_history or []
                }
        )
        
        # LLM
        response = await self.structured_llm.ainvoke(prompt)

        # Return        
        # return cast(QueryUnderstandingSchema, response)
        return QueryUnderstandingSchema.model_validate(response)