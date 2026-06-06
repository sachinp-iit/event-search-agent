# utils/batch_processor.py

import asyncio

from collections.abc import Callable


# =========================================================
# BATCH PROCESSOR
# =========================================================

class BatchProcessor:
    """
    Generic async batch processor.
    Responsibility of batch processor is:
    - Batch splitting
    - Concurrent Execution
    - Concurrency control
    - Reusable across ingetsion pipeline
    """
    
    def __init__(self, batch_size: int, max_concurrency: int):
        
        # Configuration
        self.batch_size = batch_size
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore (max_concurrency)


    # Split into batches
    async def create_batches(self, items: list) -> list[list]:
        """
        Splits a large list into configurable batch size.
        """
        
        return [
            items[index:index + self.batch_size]
            
            for index in range(0, len(items), self.batch_size)
        ]
        
    
    # Process Single Batch
    async def process_batch(self, batch: list, processor: Callable) -> None:
        """
        Executes a single batch using concurrency controls.
        """
        
        async with self.semaphore:
            await processor(batch)
        
        
    # Process all batches
    async def process_batches(self, items: list, processor: Callable) -> None:
        """
        Processess all batches concurrently.
        """
        
        # Create Batches
        batches = await self.create_batches(items = items)
        
        # Create Tasks
        tasks = [
            self.process_batch(
                batch = batch,
                processor = processor 
            )
            
            for batch in batches
        ]
        
        # Execute Concurrently
        await asyncio.gather(*tasks)