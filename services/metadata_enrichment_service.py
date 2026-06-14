# service/metadata_enrichment_service.py

from storage.metadata_loader import MetadataLoader

from schemas.event_metadata_schema import EventMetadataSchema


# =========================================================
# METADATA ENRICHMENT SERVICE
# =========================================================

class MetadataEnrichmentService:
    """
    Enriches transcript chunks with SQL Server metadata.
    - Event metadata enrichment
    - Speaker enrichment
    - Transcript metadata enrichment
    - QDrant payload preparation
    """
    
    def __init__(self, metadata_loader: MetadataLoader):
        # Dependencies
        self.metadata_loader = metadata_loader
        
        
    # Enrich Single Chunk
    async def enrich_chunk(self, chunk: dict, event_id: int) -> dict:
        
        # Load metadata
        event_metadata = await (self.metadata_loader.get_event_metadata(
            event_id = event_id
        ))
        
        # If you don't get any chunk by event_id then return the chunk as it is
        if not event_metadata:
            return chunk
        
        # Enrich Chunk
        enriched_chunk = {
            ** chunk,
            "event_id": event_metadata.event_id,
            "event_name": event_metadata.event_name,
            "event_topic": event_metadata.event_topic,
            "event_agenda": event_metadata.event_agenda,
            "domain": event_metadata.domain,
            "category": event_metadata.category,
            "event_start_date": event_metadata.event_start_date.isoformat(),
            "event_end_date": event_metadata.event_end_date.isoformat()
                if event_metadata.event_end_date
                else None,
            "author_name": event_metadata.author_name,
            "speaker_names": event_metadata.speaker_names,
            "event_company_name": event_metadata.event_company_name,
            "event_location": event_metadata.event_location,
            "transcript_location": event_metadata.transcript_location,
            "transcript_file_name": event_metadata.transcript_file_name
        }
        
        return enriched_chunk
    
    # Enrich Multiple Chunks
    async def enrich_chunks(self, chunks: list[dict], event_id: int) -> list[dict]:
        # Load Metadata Once
        event_metadata = await (self.metadata_loader.get_event_metadata(
            event_id = event_id
        ))
        
        # If you don't get any chunk by event_id then return the chunk as it is
        if not event_metadata:
            return chunks
        
        # Enrich Chunk
        enriched_chunks = []
        
        for chunk in chunks:
            enriched_chunks.append(
                {
                    ** chunk,
                    "event_id": event_metadata.event_id,
                    "event_name": event_metadata.event_name,
                    "event_topic": event_metadata.event_topic,
                    "event_agenda": event_metadata.event_agenda,
                    "domain": event_metadata.domain,
                    "category": event_metadata.category,
                    "event_start_date": event_metadata.event_start_date.isoformat(),
                    "event_end_date": event_metadata.event_end_date.isoformat()
                        if event_metadata.event_end_date
                        else None,
                    "author_name": event_metadata.author_name,
                    "speaker_names": event_metadata.speaker_names,
                    "event_company_name": event_metadata.event_company_name,
                    "event_location": event_metadata.event_location,
                    "transcript_location": event_metadata.transcript_location,
                    "transcript_file_name": event_metadata.transcript_file_name
                }
            )
            
        return enriched_chunks
  