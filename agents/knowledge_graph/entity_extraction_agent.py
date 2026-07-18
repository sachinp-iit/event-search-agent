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
        
    