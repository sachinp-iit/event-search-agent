# dependencies/transcript_loader_dependency.py

from storage.transcript_loader import (
    TranscriptLoader
)

from config.settings import settings


# =========================================================
# TRANSCRIPT LOADER DEPENDENCY
# =========================================================

async def transcript_loader_dependency() -> TranscriptLoader:
    """
    Dependency provider for TranscriptLoader
    """
    
    return TranscriptLoader (
        transcript_directory = settings.RAW_TRANSCRIPTS_DIRECTORY
    )