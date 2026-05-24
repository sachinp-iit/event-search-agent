# utils/validators.py

from fastapi import HTTPException

# ================================================
# VALIDATE TEXT INPUT
# ================================================

async def validate_text_input(
    text: str
) -> None:
    
    """
    Async validation guardrails for embedding and LLM inputs.
    
    Validations:
    - None protection
    - Empty input protection
    - Whitespace protection
    - Minimum length validation
    - Maxium length validation
    """
    
    # None Validation
    
    if text is None:
        
        raise HTTPException(
            status_code = 400,
            detail = "Input text cannot be None."
        )
        
    # Whitespace Validation
    
    cleaned_text = text.strip()
    
    if not cleaned_text:
        
        raise HTTPException(
            status_code = 400,
            detail = "Input text cannot be empty."
        )
        
    # Minimum Length Validation
    
    if len(cleaned_text) < 3:
        
        raise HTTPException(
            status_code = 400,
            detail = "Input text is too short."
        )
        
    # Maximum Length Validation
    
    if len(cleaned_text) > 10000:
        
        raise HTTPException(
            status_code = 400,
            detail = "Input text exceeds allowed limit."
        )