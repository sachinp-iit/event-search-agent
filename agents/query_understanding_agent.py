# agent/query_understanding_agent.py

from langchain_core.language_models.chat_models import BaseChatModel

from prompts.prompt_manager import render_prompt


# =========================================================
# QUERY UNDERSTANDING AGENT
# =========================================================
class QueryUnderstadingAgent:
    """
    Responsible for understanding the user's natural language query.
    - Intent Detection
    - Query Classification
    - Domain Detection
    - Metadata Extraction
    - Filter Extraction
    - Query Normalization
    """
    
    def __init__(self, llm: BaseChatModel):
        
        self.llm = llm
        
    # Analyze Query
    async def analyze_query(self, user_query: str) -> dict:
        # Load Prompt
        prompt = render_prompt (
            template_name = (
                "agents/"
                "query_understanding_prompt.jinja2" # TODO Replace with Enum Constants later
                ),
            variables = {"user_query": user_query}
        )
        
        # LLM
        response = await self.llm.ainvoke(prompt)

        # TODO: Replace wih structured output using Pydantic + Guardrails
        return {
            "analysis": response.content
        }