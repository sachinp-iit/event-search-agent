# dependency/vector_indexer_dependency.py

from fastapi import Depends

from qdrant_client import AsyncQdrantClient

from langchain_core.embeddings import Embeddings

from dependencies.qdrant_dependency import qdrant_client_dependency

from dependencies.embedding_dependency import (
    embedding_model_dependency
)

from vector_db.vector_indexer import VectorIndexer

# =========================================================
# VECTOR INDEXER DEPENDENCY
# =========================================================

async def vector_indexer_dependency (
    
    qdrant_client: AsyncQdrantClient = Depends (
        qdrant_client_dependency
    ),

    embedding_model: Embeddings = Depends (
        embedding_model_dependency
    )
) -> VectorIndexer:
    """
    Dependency provider for VectorIndexer.
    """
    
    return VectorIndexer (
        qdrant_client = qdrant_client,
        embedding_model = embedding_model
    )
    