# dependency/answer_generation_dependency.py

from fastapi import Depends

from langchain_core.language_models.chat_models import BaseChatModel

from dependencies.llm_dependency import get_llm

from agents.answer_generation_agent import AnswerGenerationAgent


# =========================================================
# ANSWER GENERATION AGENT DEPENDENCY
# =========================================================

def get_answer_generation_agent(
    llm: BaseChatModel = Depends(get_llm)
    ) -> AnswerGenerationAgent:
    
    return AnswerGenerationAgent(llm = llm)