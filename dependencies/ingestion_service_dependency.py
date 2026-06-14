# dependencies/ingestion_service_dependency.py

from fastapi import Depends

from services.ingestion_service import IngestionService

from storage.metadata_loader import MetadataLoader

from pipelines.batch_ingestion_pipeline import BatchIngestionPipeline

from dependencies.batch_ingestion_pipeline_dependency import batch_ingestion_pipeline_dependency

from dependencies.metadata_loader_dependency import metadata_loader_dependency


# =========================================================
# INGESTION SERVICE DEPENDENCY
# =========================================================
async def ingestion_service_dependency(
    
    metadata_loader: MetadataLoader = Depends(
        metadata_loader_dependency
    ),
    
    ingestion_pipeline: BatchIngestionPipeline = Depends (
        batch_ingestion_pipeline_dependency
    )    
) -> IngestionService:
    
    """
    Dependency provider for IngestionService
    """
    
    return IngestionService (
        metadata_loader = metadata_loader,
        ingestion_pipeline = ingestion_pipeline
    )