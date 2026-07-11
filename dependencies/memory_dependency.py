# dependency/memory_dependency.py

from memory.memory_manager import MemoryManager

# =========================================================
# GLOBAL MEMORY MANAGER
# =========================================================
memory_manager = MemoryManager()

# =========================================================
# MEMORY MANAGER DEPENDENCY
# =========================================================

def get_memory_manager() -> MemoryManager:
    return memory_manager