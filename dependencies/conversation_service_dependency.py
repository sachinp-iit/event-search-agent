# dependency/conversation_service_dependency.py

from services.conversation_service import ConversationService

from dependencies.conversation_summarizer_dependency import get_conversation_summarizer


# =========================================================
# CONVERSATION SUMMARIZER SERVICE DEPENDENCY
# =========================================================

_conversation_service: ConversationService | None = None

def get_conversation_service() -> ConversationService:
    """
    Return a singleton instance of the ConversationService
    """
    
    global _conversation_service
    
    if _conversation_service is None:
        _conversation_service = ConversationService(
            conversation_summarizer=get_conversation_summarizer()
        )
        
    return _conversation_service
    