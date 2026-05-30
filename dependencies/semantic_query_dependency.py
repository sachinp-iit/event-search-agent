# dependencies/semantic_query_dependency.py

from fastapi import Depends

from qdrant_client import AsyncQdrantClient

from langchain_core.embeddings import Embeddings

from dependencies.qdrant_dependency import (
    qdrant_client_dependency
)

from dependencies.embedding_dependency import (
    embedding_model_dependency
)

from vector_db.semantic_query import (
    SemanticQueryEngine
)

# =========================================================
# SEMANTIC QUERY ENGINE DEPENDENCY
# =========================================================

async def semantic_query_dependency (
    qdrant_client: AsyncQdrantClient = Depends (
        qdrant_client_dependency
    ),
    
    embedding_model: Embeddings = Depends (
        embedding_model_dependency
    )
) -> SemanticQueryEngine:
    
    return SemanticQueryEngine (
        qdrant_client = qdrant_client,
        embedding_model = embedding_model
    )