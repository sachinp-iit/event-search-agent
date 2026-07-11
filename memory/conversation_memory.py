# memory/conversation_memory.py

from collections import deque

from config.settings import settings

# =========================================================
# CONVERSATION MEMORY
# =========================================================

class ConversationMemory:
    
    def __init__(self, max_history = settings.MAX_HISTORY) -> None:
        self._history = deque(maxlen=max_history)
        
    # Add Message
    def add_message(self, role: str, content: str) -> None:
        self._history.append(
            {
                "role": role,
                "content": content
            }
        )
        
    # Get History
    def get_history(self) -> list[dict]:
        return list(self._history)
    
    # Clear History
    def clear(self) -> None:
        self._history.clear()