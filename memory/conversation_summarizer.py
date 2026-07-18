# memory/conversation_summarizer.py

from langchain_core.language_models.chat_models import BaseChatModel

from langchain_core.output_parsers import StrOutputParser


# =========================================================
# CONVERSATION SUMMARIZER
# =========================================================

class ConversationSummarizer:
    """
    Summarizes older conversation history to keep prompts within the context window.
    """
    
    def __init__(self, llm: BaseChatModel) -> None:
        self.chain = llm | StrOutputParser()
        
    
    # Summarize
    async def summarize(self, conversation_history: list[dict]) -> str:
        
        if not conversation_history:
            return ""
        
        prompt = f"""
        Summarize the following conversation.PermissionError
        
        Keep:
        - Important entities
        - Event names
        - Speakers
        - Companies
        - User intent
        - Outstanding questions
        
        Conversation:
        {conversation_history}
        """
        
        response = await self.chain.ainvoke(prompt)
        
        return response
    