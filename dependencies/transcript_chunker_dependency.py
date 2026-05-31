# dependencies/transcript_chunker_dependency.py

from utils.chunking import (
    TranscriptChunker
)


# =========================================================
# TRANSCRIPT CHUNKER DEPENDENCY
# =========================================================

async def transcript_chunker_dependency() -> TranscriptChunker:
    """
    Dependency provider for TranscriptChunker
    """
    
    return TranscriptChunker()

