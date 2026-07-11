# memory/memory_prompt_helper.py

from memory.conversation_memory import ConversationMemory

from config.settings import settings

# =========================================================
# MEMORY PROMPT HELPER
# =========================================================
class MemoryPromptHelper:
    """
    Converts conversation history into a prompt-friendly format
    while limiting context size.
    """
    def __init__(self, max_messages = settings.MAX_HISTORY) -> None:
        self.max_messages = max_messages
        
    # Build Context
    def build_context(self, memory: ConversationMemory) -> list[dict]:
        """
        Returns the most recent conversation messages.
        """
        history = memory.get_history()
        
        if len(history) <= self.max_messages:
            return history
        
        return history[-self.max_messages:]
    
    # Build Text
    def build_text(self, memory: ConversationMemory) -> str:
        """
        Returns formatted conversation history.
        """
        history = self.build_context(memory)
        lines: list[str] = []
        
        for message in history:
            lines.append(
                f"{message['role'].upper()}: "
                f"{message['content']}"
            )
            
        return "\n\n".join(lines)
        
        
        
    
    