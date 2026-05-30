# dependency/embedding_generator_dependency.py

from fastapi import Depends

from langchain_core.embeddings import Embeddings

from dependencies.embedding_dependency import (
    embedding_model_dependency
)

from models.embedding.embedding_generator import (
    EmbeddingGenerator
)


# =========================================================
# EMBEDDING GENERATOR DEPENDENCY
# =========================================================

async def embedding_generator_dependency (
    
    embedding_model: Embeddings = Depends (
        embedding_model_dependency
    )
) -> EmbeddingGenerator:
    
    return EmbeddingGenerator (
        embedding_model = embedding_model
    )