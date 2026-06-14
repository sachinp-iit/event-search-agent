# scripts/ingest_transcripts.py

import asyncio

from core.container import container


# =========================================================
# INGESTION ENTRYPOINT
# =========================================================

async def main() -> None:
    
    # Initialize Application
    await container.initialize()
    
    # Start Ingestion
    await (container.ingestion_service.ingest_all_events())

    print("Transcript ingestion completed successfully.")
    
# Script Entrypoint
if __name__ == "__main__":
    asyncio.run(main())
    

# =========================================================
# EXECUTION COMMAND
# =========================================================
# from command prompt you execute following command to ingest 
# all your transcripts from a "raw_transcripts" folder.
# python scripts/ingest_transcripts.py