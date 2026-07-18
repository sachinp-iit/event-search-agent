# dependency/conversation_summarizer_dependency.py

from memory.conversation_summarizer import ConversationSummarizer
from dependencies.llm_dependency import get_llm


# =========================================================
# CONVERSATION SUMMARIZER DEPENDENCY
# =========================================================

_conversation_summarizer: ConversationSummarizer | None = None

def get_conversation_summarizer() -> ConversationSummarizer:
    global _conversation_summarizer
    
    if _conversation_summarizer is None:
        _conversation_summarizer = ConversationSummarizer(llm = get_llm())
        
    return _conversation_summarizer