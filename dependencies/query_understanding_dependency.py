# dependency/query_understanding_dependency.py

from fastapi import Depends

from langchain_core.language_models.chat_models import BaseChatModel

from agents.query_understanding_agent import QueryUnderstadingAgent

from dependencies.llm_dependency import get_llm


# =========================================================
# QUERY UNDERSTANDING AGENT DEPENDENCY
# =========================================================

def get_query_understanding_agent(
    llm: BaseChatModel = Depends (get_llm)
) -> QueryUnderstadingAgent:
    
    return QueryUnderstadingAgent(llm = llm)