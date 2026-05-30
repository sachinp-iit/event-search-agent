# utils/chunking.py

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import settings


# ================================================
# TRANSCRIPT CHUNKER
# ================================================

class TranscriptChunker:
    def __init__(self):
        
        self.text_splitter = (
            RecursiveCharacterTextSplitter (
                
                chunk_size = settings.CHUNK_SIZE,
                chunk_overlap = settings.CHUNK_OVERLAP,
                
                separators = [
                    "\n\n",
                    "\n",
                    ". ",
                    " "
                ]
            )
        )
        
        
    # Chunk Transcript
    async def chunk_transcript(self, transcript_text: str) -> list[str]:
        
        chunks = self.text_splitter.split_text(
            transcript_text
        )
        
        return chunks
    
    
    # Chunk Mutiple Transcripts
    async def chunk_transcripts(self, transcripts: list[dict]) -> list[dict]:
        
        processed_chunks = []
        
        for transcript in transcripts:
            
            chunks = await self.chunk_transcript (
                transcript["content"]
            )
            
            for chunk in chunks:
                
                processed_chunks.append(
                    {
                        "file_name": transcript["file_name"],
                        "transcript_text": chunk
                    }
                )
                
        return processed_chunks