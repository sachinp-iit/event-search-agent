# dependency/memory_prompt_helper_dependency.py

from memory.memory_prompt_helper import MemoryPromptHelper

# =========================================================
# MEMORY PROMPT HELPER
# =========================================================
memory_prompt_helper = MemoryPromptHelper()


# =========================================================
# MEMORY PROMPT HELPER DEPENDENCY
# =========================================================
def get_memory_prompt_helper() -> MemoryPromptHelper:
    return memory_prompt_helper