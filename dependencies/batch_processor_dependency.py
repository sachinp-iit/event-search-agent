# dependencies/batch_processor_dependency.py

from utils.batch_processor import BatchProcessor

from config.settings import settings


# =========================================================
# BATCH PROCESSOR DEPENDENCY
# =========================================================

async def batch_processor_dependency() -> BatchProcessor:
    """
    Dependency provider for BatchProcessor.
    Responsibilities:
    - Batch creation
    - Concurrent execution
    - Concurrency throttling
    """
    
    return BatchProcessor(
        batch_size = settings.INGESTION_BATCH_SIZE,
        max_concurrency = settings.MAX_CONCURRENT_BATCHES
    )