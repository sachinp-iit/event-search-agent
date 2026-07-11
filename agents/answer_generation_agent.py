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
