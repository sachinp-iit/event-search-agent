# dependencies/llm_dependency.py

from models.llm.openrouter_client import llm


# =========================================================
# LLM DEPENDENCY PROVIDER
# =========================================================

def get_llm():
    
    """
    Provides shared OpenRouter LLM instance across routes, services, and agents.
    """
    
    return llm
    