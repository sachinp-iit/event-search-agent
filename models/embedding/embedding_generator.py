# models/embedding/embedding_generator.py

from langchain_core.embeddings import Embeddings

from utils.validators import validate_text_input


# ================================================
# EMBEDDING GENERATOR
# ================================================

class EmbeddingGenerator:
    
    def __init__(
        self,
        embedding_model: Embeddings
    ):
        
        self.embedding_model = embedding_model
        
    # Generate Single Embedding
    
    async def generate_embedding(self, text: str) -> list[float]:
        
        """
        Generates semantic embedding for a single text input.
        """
        
        # Input validation/guardrails
        await validate_text_input(text = text)
        
        # Embedding generation
        embedding = await self.embedding_model.aembed_query(
            text = text
        )
        
        return embedding
    
    
    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generates semantic embeddings for multiple text inputs.
        """
        
        # Input validation / guardrails
        
        for text in texts:
            await validate_text_input(text = text)
        
        # Embedding Generation
        embeddings = await self.embedding_model.aembed_documents(
            texts = texts
        )
        
        return embeddings
        