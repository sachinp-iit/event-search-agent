# schemas/event_metadata_schema.py

from datetime import datetime

from pydantic import BaseModel

from pydantic import Field


# =========================================================
# EVENT METADATA SCHEMA
# =========================================================

class EventMetadataSchema(BaseModel):
    """
    Master event metadata schema.
    """
    event_id: int
    event_name: str
    event_topic: str
    event_agenda: str | None = None
    domain: str | None = None
    category: str | None = None
    event_start_date: datetime
    event_end_date: datetime | None = None
    
    moderator_name: str | None = None
    author_name: str | None = None
    speaker_names: list[str] = Field(default_factory=list)
    
    event_company_name: str | None = None
    event_location: str | None = None
    
    transcript_location: str
    transcript_file_name: str
    
    created_at: datetime | None = None
    updated_at: datetime | None = None
    