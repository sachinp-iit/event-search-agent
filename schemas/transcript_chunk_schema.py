# schemas/transcript_chunk_schema.py

from pydantic import BaseModel
from pydantic import Field


# =========================================================
# TRANSCRIPT CHUNK SCHEMA
# =========================================================

class TranscriptChunkSchema(BaseModel):
    
    # Event Metadata
    
    event_name: str | None = None
    event_topic: str | None = None
    speaker_name: str | None = None
    event_date: str | None = None
    event_company: str | None = None
    event_location: str | None = None
    domain: str | None = None
    category: str | None = None
    file_name: str | None = None
    
    # Transcript Content
    transcript_text: str = Field (min_length=1, description = "Transcript chunk text")
    
    # Chunk Metadata
    chunk_id: str | None = None
    chunk_sequence: int | None = None