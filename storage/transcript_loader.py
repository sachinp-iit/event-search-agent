# storage/transcript_loader.py

from pathlib import Path

import aiofiles


# =========================================================
# TRANSCRIPT LOADER
# =========================================================

class TranscriptLoader:
    
    def __init__(self, transcript_directory: str):
        
        self.transcript_directory = Path (
            transcript_directory
        )
        
    
    # Load Single Transcript    
    async def load_transcript(self, file_name: str) -> str:
        
        transcript_path = (
            self.transcript_directory / file_name
        )
        
        async with aiofiles.open (transcript_path, mode = "r", encoding = "utf-8") as file:
            
            transcript_content = await file.read()
            
        return transcript_content
    
    
    # Load All Transcripts
    async def load_all_transcripts(self) -> list[dict]:
        
        transcripts = []
        
        for transcript_file in self.transcript_directory.glob ("*.txt"):
            
            async with aiofiles.open(transcript_file, mode = "r", encoding = "utf-8") as file:
                
                transcript_content = await file.read()
                
            transcripts.append(
                {
                    "file_name": transcript_file.name,
                    "content": transcript_content
                }
            )
            
        return transcripts
        
    
    