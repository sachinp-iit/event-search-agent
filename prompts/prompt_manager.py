# prompts/prompt_manager.py

from pathlib import Path

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


# =========================================================
# PROMPTS ROOT DIRECTORY
# =========================================================

PROMPT_ROOT_DIRECTORY = Path("prompts")


# =========================================================
# JINJA2 ENVIRONMENT
# =========================================================

jinja_environment = Environment(
    loader=FileSystemLoader(PROMPT_ROOT_DIRECTORY),
    
    autoescape=select_autoescape(),
    
    trim_blocks=True,
    
    lstrip_blocks=True
)


# =========================================================
# GENERIC PROMPT RENDERER
# =========================================================

def render_prompt(
    template_name: str,
    variables: dict
) -> str:
    
    """
    Dynamically loads and renders
    Jinja2 prompt templates.
    
    Supports:
    - Reusable prompts
    - Dynamic variable injection
    - Multi-agent prompt orchestration
    - Centralized prompt management
    - Easier testing and debugging
    """
    
    template = jinja_environment.get_template(template_name)
    
    rendered_prompt = template.render(**variables)
    
    return rendered_prompt