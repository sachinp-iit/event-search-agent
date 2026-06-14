# services/ingestion_service.py

from pipelines.batch_ingestion_pipeline import BatchIngestionPipeline

from storage.metadata_loader import MetadataLoader


# =========================================================
# INGESTION SERVICE
# =========================================================

class IngestionService:
    """
    Coordinates the end-to-end ingestion workflow.
    """
    
    def __init__(self, metadata_loader: MetadataLoader, ingestion_pipeline: BatchIngestionPipeline):
        self.metadata_loader = metadata_loader
        self.ingestion_pipeline = ingestion_pipeline
        
    
    # Ingest All Events
    async def ingest_all_events(self) -> None:
        
        events = await(self.metadata_loader.get_all_events())
        
        for event in events:
            await self.ingestion_pipeline.ingest_event(
                event_id = event.event_id,
                transcript_file_name = event.transcript_file_name
            )
    
            
    # Ingest Single Event
    async def ingest_event(self, event_id: int) -> None:
        event = await(self.metadata_loader.get_event_metadata(event_id=event_id))
        
        if not event:
            return
        
        await self.ingestion_pipeline.ingest_event(
            event_id = event_id,
            transcript_file_name = event.transcript_file_name
        )