# storage/metadata_loader.py

from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.event_metadata_schema import EventMetadataSchema


# =========================================================
# METADATA LOADER
# =========================================================

class MetadataLoader:
    """
    Loads event metadata from SQL Server.
    """
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    
    # Get Event Metadata
    async def get_event_metadata(self, event_id: int) -> EventMetadataSchema | None:
        
        # Event Query
        query = text("""
                     SELECT e.EventId, e.EventName, e. EventTopic, e.EventAgenda,
                     e.DomainName, e.CategoryName, e.EventStartDate, e.EventEndDate,
                     e.AuthorName, e.EventCompanyName, e.EventLocation,
                     t.TranscriptLocation, t.TranscriptFileName
                     FROM Events e
                     INNER JOIN Transcripts t ON e.EventId = t.EventId
                     WHERE e.EventId = :event_id
                     """)
        
        result = await self.db_session.execute(
            query, {"event_id": event_id}
        )

        event_row = result.mappings().first()
        
        # If don't get any data
        if not event_row:
            return None
        
        # Speakers
        speaker_query = text("""
                             SELECT s.SpeakerName FROM EventSpeakers es
                             INNER JOIN Speakers s ON es.SpeakerId = s.SpeakerId
                             WHERE es.EventId = :event_id
                             """)
        
        speaker_result = await self.db_session.execute(
            speaker_query, {"event_id": event_id}
        )

        speakers = [ row["SpeakerName"] for row in speaker_result.mappings().all()]
        
        # Build Metadata Schema
        return EventMetadataSchema(
            event_id = event_row["EventId"],
            event_name = event_row["EventName"],
            event_topic = event_row["EventTopic"],
            event_agenda = event_row["EventAgenda"],
            domain = event_row["DomainName"],
            category = event_row["CategoryName"],
            event_start_date = event_row["EventStartDate"],
            event_end_date = event_row["EventEndDate"],
            author_name = event_row["AuthorName"],
            speaker_names = speakers,
            event_company_name = event_row["EventCompanyName"],
            event_location = event_row["EventLocation"],
            transcript_location = event_row["TranscriptLocation"],
            transcript_file_name = event_row["TranscriptFileName"]
        )
        
    # Get All Events
    async def get_all_events(self) -> list[EventMetadataSchema]:
        
        query = text("""
                     SELECT EventId FROM Events
                     """)
        
        result = await self.db_session.execute(query)
        
        event_ids = [ row["EventId"] for row in result.mappings().all()]
        
        events = []
        
        for event_id in event_ids:
            event = await self.get_event_metadata(event_id = event_id)
            
            if event:
                events.append(event)
                
        return events
    