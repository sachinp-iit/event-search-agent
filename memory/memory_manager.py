# memory/memory_manager.py

from memory.conversation_memory import ConversationMemory

# =========================================================
# MEMORY MANAGER
# =========================================================
class MemoryManager:
    """
    Maintains conversation memory per user/session.
    """
    def __init__(self) -> None:
        self._sessions: dict[str, ConversationMemory] = {}
        
        
    # Get Memory
    def get_memory(self, session_id: str) -> ConversationMemory:
        
        if session_id not in self._sessions:
            self._sessions[session_id] = ConversationMemory()
            
        return self._sessions[session_id]
    
    # Remove Memory
    def remove_memory(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
        
    
    # Clear All
    def clear_all(self) -> None:
        
        self._sessions.clear()