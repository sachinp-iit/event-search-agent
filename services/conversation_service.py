# services/conversation_service.py

from memory.conversation_memory import ConversationMemory
from memory.conversation_summarizer import ConversationSummarizer


# =========================================================
# CONVERSATION SUMMARIZER SERVICE
# =========================================================

class ConversationService:
    """
    Orchestrates conversation-related operations.
    """
    
    def __init__(self, conversation_summarizer: ConversationSummarizer) -> None:
        self.conversation_summarizer = conversation_summarizer
    
    async def summarize_conversation(self, memory: ConversationMemory) -> str:
        """
        Generate a summary of the current conversation history.
        """
        
        converation_history = memory.get_history()
        
        if not converation_history:
            return ""
        
        return await self.conversation_summarizer.summarize(
            conversation_history=converation_history
        )