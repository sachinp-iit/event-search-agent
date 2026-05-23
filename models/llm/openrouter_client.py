# models/llm/openrouter_client.py

from langchain_openai import ChatOpenAI

from config.settings import settings


# =========================================================
# OPENROUTER LLM INITIALIZATION
# =========================================================

llm = ChatOpenAI (
    model = settings.OPENROUTER_MODEL,
    
    api_key = settings.OPENROUTER_API_KEY,
    
    base_url = settings.OPENROUTER_BASE_URL,
    
    temperature = 0.3,
    
    default_headers = {
        "HTTP-Referer": settings.OPENROUTER_HEADER_HTTP_REFERER,
        "X-Title": settings.OPENROUTER_HEADER_HTTP_X_TITLE
    }
)


# =========================================================
# GENERATE LLM REPONSE
# =========================================================

def generate_llm_response(user_query: str) -> str:
    response = llm.invoke(user_query)
    
    return response.content