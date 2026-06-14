# dependencies/metadata_enrichment_service_dependency.py

from fastapi import Depends

from storage.metadata_loader import MetadataLoader

from services.metadata_enrichment_service import MetadataEnrichmentService

from dependencies.metadata_loader_dependency import metadata_loader_dependency



# =========================================================
# METADATA ENRICHMENT SERVICE
# =========================================================

async def metadata_enrichment_service_dependency(
    metadata_loader: MetadataLoader = Depends (
        metadata_loader_dependency
    )
) -> MetadataEnrichmentService:
    """
    Dependency provider for MetadataEnrichmentService.
    """
    
    return MetadataEnrichmentService (metadata_loader = metadata_loader)
    