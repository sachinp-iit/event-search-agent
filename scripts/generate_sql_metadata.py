# scripts/generate_sql_metadata.py

import asyncio

import json

import re

from pathlib import Path

from datetime import datetime

import aiofiles

from sqlalchemy import text

from config.settings import settings

from database.sql_server_client import get_db_session

from models.llm.openrouter_client import llm


# =========================================================
# CONSTANTS
# =========================================================

TRNSCRIPT_DIRECTORY = Path (settings.RAW_TRANSCRIPTS_DIRECTORY)

EPISODE_PATTERN = re.compile(r"Episode\s+(\d+)", re.IGNORECASE)

TITLE_PATTERN = re.compile(r"Episode\s+\d+\s*[:-]\s*(.+)", re.IGNORECASE)

SPEAKER_PATTERN = re.compile(r"^([A-Z][A-Za-z] .'-]+):", re.MULTILINE)

COMPANY_PATTERN = re.compile(r"(?:from|at)\s+([A-Z][A-Za-z0-9& .-]+)", re.IGNORECASE)


# =========================================================
# READ TRANSCRIPT
# =========================================================

async def load_transcript(transcript_file: Path) -> str:
    """
    Reads transcript from disk.
    """
    
    async with aiofiles.open(transcript_file, mode = "r", encoding = "utf-8") as file:
        transcript = await file.read()
        
    return transcript


# =========================================================
# REMOVING DUPLICATES
# =========================================================

def unique(values: list[str]) -> list[str]:
    """
    Removes duplicate values while maintaining the order.
    """
    
    seen = set()
    
    results = []
    
    for value in values:
        value = value.strip()
        
        if not value:
            continue
        
        if value in seen:
            continue
        
        seen.add(value)
        results.append(value)

    return results

# =========================================================
# PARSE EPISODE NUMBER
# =========================================================

def parse_episode_number(transcript_file: Path) -> int:
    
    match = EPISODE_PATTERN.search(transcript_file.stem)
    
    if not match:
        raise ValueError(f"Episode number not found: {transcript_file.name}")
    
    return int(match.group(1).strip())


# =========================================================
# BUILD EXTRACTION CONTEXT
# =========================================================

def build_extraction_context(
    transcript_file: Path,
    transcript: str
) -> dict:

    return {
        "event_id": parse_episode_number(transcript_file),
        "transcript_file_name": transcript_file.name,
        "transcript_location": str(transcript_file),
        "transcript": transcript
    }
    



# =========================================================
# FALLBACK EVENT NAME
# =========================================================

def extract_event_name(transcript: str, transcript_file: Path) -> str:
    """
    Deterministically extract an event title from the transcript.
    Falls back to the filename if no title is found.
    """
    for line in transcript.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("zero knowledge"):
            return line
        if line.lower().startswith("episode"):
            return line

    match = TITLE_PATTERN.search(transcript)
    if match:
        return match.group(1).strip()

    return transcript_file.stem

# =========================================================
# EXTRACT METADATA USING OPENROUTER
# =========================================================

async def extract_metadata(extraction_context: dict) -> dict:
    
    prompt = f"""
    You are an expert information extraction system.
    Extract metadata from the podcast transcript.
    Return ONLY valid JSON.
    
    {{
        "event_name": "...",
        "event_topic": "...",
        "event_agenda": "...",
        "domain": "...",
        "category": "...",
        "author_name": "...",
        "speaker_names": "...",
        "event_company_name": "...",
        "event_location": "...",
        
        "confidence": {{
            "event_name": 0.0,
            "event_topic": 0.0,
            "event_agenda": 0.0,
            "domain": 0.0,
            "category": 0.0,
            "author_name": 0.0,
            "speaker_names": 0.0,
            "event_company_name": 0.0,
            "event_location": 0.0
        }}
    }}
    
    Rules:

    1. Return ONLY valid JSON.
    2. Do not hallucinate.
    3. event_name is REQUIRED whenever a title exists.
    4. speaker_names must be an array.
    5. Return [] when there are no guest speakers.
    6. Use null only for optional fields.
    
    Transcript:
    
    {extraction_context["transcript"]}
    """
    
    response = await llm.ainvoke(prompt)
    
    content = response.content
    
    if isinstance(content, list):
        text = ""
        
        for item in content:
            if isinstance(item, dict):
                text += item.get("text","")
            else:
                text += getattr(item, "text", str(item))
        
        content = text
        
    content = content.strip()
    
    # Remove markdown/fences if available in the response
    if content.startswith("```json"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        
    elif content.startswith("```"):
        content = content.replace("```", "")
        
    content = content.strip()
    
    # Parse JSON
    metadata = json.loads(content)
    
    metadata["event_id"] = (extraction_context["event_id"])
    metadata["transcript_file_name"] = (extraction_context["transcript_file_name"])
    metadata["transcript_location"] = (extraction_context["transcript_location"])
    
    return metadata


# =========================================================
# EXTRACT METADATA USING OPENROUTER
# =========================================================

async def save_metadata(metadata: dict) -> None:
    
    async for session in get_db_session():
        
        # Insert Event
        event_result = await session.execute(
            text("""
            
            INSERT INTO Events (
                EventName,
                EventTopic,
                EventAgenda,
                DomainName,
                CategoryName,
                EventStartDate,
                EventEndDate,
                AuthorName,
                EventCompany,
                EventLocation
            )
            
            OUTPUT INSERTED.EventId
            
            VALUES (
                
                :event_name,
                :event_topic,
                :event_agenda,
                :domain,
                :category,
                GETUTCDATE(),
                GETUTCDATE(),
                :author_name,
                :event_company_name,
                :event_location
            )
            """),
            
            {
                "event_name": metadata.get("event_name"),
                "event_topic": metadata.get("event_topic"),
                "event_agenda": metadata.get("event_agenda"),
                "domain": metadata.get("domain"),
                "category": metadata.get("category"),
                "author_name": metadata.get("author_name"),
                "event_company_name": metadata.get("event_company_name"),
                "event_location": metadata.get("event_location")
            }
        )
        
        event_id = event_result.scalar_one()
        
        # Insert Speakers
        speakers = metadata.get("speaker_names") or []
        
        if isinstance(speakers, str):
            speakers = [speakers]
        
        for speaker in speakers:
            existing = await session.execute(
                text("""
                     
                     SELECT SpeakerId FROM Speakers
                     WHERE SpeakerName = :speaker
                     
                     """),
                {
                    "speaker": speaker
                }
            )
            
            speaker_id = existing.scalar_one_or_none()
        
            if speaker_id is None:
                inserted = await session.execute(
                    text("""
                        
                        INSERT INTO Speakers (SpeakerName)
                        
                        OUTPUT INSERTED.SpeakerId
                        VALUES(:speaker)
                        """),
                    
                    {
                        "speaker": speaker
                    }
                )
            
                speaker_id = inserted.scalar_one()
        
            # EVENT SPEAKER
            await session.execute(
                
                text("""
                    
                    INSERT INTO EventSpeakers (EventId, SpeakerId)
                    VALUES (:event_id, :speaker_id)
                    
                    """),                
                    {
                        "event_id": event_id,
                        "speaker_id": speaker_id
                    }
            )
        
        # INSERT TRANSCRIPT METADATA
        await session.execute(
            text("""
                 
                 INSERT INTO Transcripts (EventId, TranscriptLocation, TranscriptFileName)
                 VALUES (:event_id, :transcript_location, :transcript_file_name)
                 """),
            {
                "event_id": event_id,
                "transcript_location": metadata.get("transcript_location"),
                "transcript_file_name": metadata.get("transcript_file_name")
            }
        )
        
        await session.commit()
        
# =========================================================
# PROCESS SINGLE TRANSCRIPT
# =========================================================

async def process_transcript(transcript_file: Path) -> None:
    
    print(f"Processing {transcript_file.name}...")
    
    transcript = await load_transcript(transcript_file)
    
    extraction_context = build_extraction_context(
        transcript_file,
        transcript
    )
    
    metadata = await extract_metadata(extraction_context)

    # Deterministic fallback for missing title
    if not metadata.get("event_name"):
        metadata["event_name"] = extract_event_name(
            transcript,
            transcript_file
        )

    # Prevent SQL truncation if the database column is smaller.
    if metadata.get("event_name"):
        metadata["event_name"] = metadata["event_name"][:300]

    await save_metadata(metadata)
    
    print(f"Completed {transcript_file.name}...")
    

# =========================================================
# MAIN
# =========================================================

async def main() -> None:
    
    transcript_files = sorted(Path(settings.RAW_TRANSCRIPTS_DIRECTORY).glob("*.txt"))
    
    print(f"Found {len(transcript_files)} transcript(s).")
    
    for transcript_file in transcript_files:
        try:
            await process_transcript(transcript_file)
            
        except Exception as ex:
            print(f"Failed: {transcript_file.name}")
            print(ex)
            
    print("\nMetadata generation completed.")
    

# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    asyncio.run(main())
    
    
# =========================================================
# NOTES - HOW TO RUN THIS FILE
# =========================================================
# python -m scripts.generate_sql_metadata