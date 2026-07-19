# Event Metadata Repository

## Overview

This repository implements the foundational metadata layer for an Event Intelligence platform. It consists of:

- A SQL Server schema that stores event, speaker, and transcript metadata.
- An asynchronous SQLAlchemy client that provides efficient and scalable database connectivity for Python applications.

The repository is intentionally focused on **structured metadata** rather than transcript content. Transcript files are expected to be stored in external storage, while this database maintains their metadata and relationships.

---

# Architecture

```text
                    Client / API
                         │
                         ▼
                Service / Repository Layer
                         │
                         ▼
               get_db_session() Provider
                         │
                         ▼
             SQLAlchemy AsyncSession Factory
                         │
                         ▼
             SQLAlchemy Async Engine
                         │
                         ▼
                  SQL Server Database
       ┌──────────────┬───────────────┬──────────────┐
       │              │               │              │
    Events        Speakers     EventSpeakers    Transcripts
```

---

# Components

## 1. SQL Server Client

The `sql_server_client.py` module encapsulates all database connectivity.

### Responsibilities

- Creates a singleton asynchronous SQLAlchemy engine.
- Manages database connection pooling.
- Provides reusable asynchronous sessions.
- Supplies sessions through dependency injection using `get_db_session()`.

### Connection Pool

| Setting | Purpose |
|---------|---------|
| pool_size=10 | Keeps up to 10 active connections ready. |
| max_overflow=20 | Allows temporary expansion during peak load. |
| pool_pre_ping=True | Validates connections before use, preventing stale connection errors. |

---

# Database Design

The schema follows a normalized relational model.

## Events

The **Events** table is the primary entity.

It stores descriptive information about an event that can later be searched, categorized, processed by AI models, or linked to transcript data.

### Stored information

- Event name
- Topic
- Agenda
- Domain
- Category
- Author
- Company
- Location
- Start and end dates
- Audit timestamps

This table acts as the parent entity for transcripts and speaker mappings.

---

## Speakers

The **Speakers** table stores reusable speaker information.

Instead of duplicating speaker details across events, each speaker is stored once and referenced through a junction table.

This design supports:

- One speaker participating in multiple events
- Consistent speaker metadata
- Reduced data duplication

Speaker attributes include:

- Name
- Title
- Company
- Creation timestamp

---

## EventSpeakers

This table implements the many-to-many relationship between Events and Speakers.

### Why it exists

An event may have several speakers.

Likewise, a speaker may appear in many different events.

Instead of storing multiple speaker IDs in the Events table, this bridge table maintains normalized relationships.

```text
Events
   │
   │ 1
   ▼
EventSpeakers
   ▲
   │ *
Speakers
```

---

## Transcripts

The **Transcripts** table stores transcript metadata.

It does **not** store transcript text.

Instead it records:

- Associated event
- Transcript storage location
- File name
- Version number
- Auto moderation status
- Creation timestamp

Keeping transcript content outside the database reduces database size while allowing transcript files to reside in Blob Storage, Data Lakes, or other document repositories.

---

# Relationships

```text
Events (1)
   │
   ├──────────────► Transcripts (Many)
   │
   └──────────────► EventSpeakers (Many)
                          │
                          ▼
                     Speakers
```

---

# Indexing Strategy

The schema defines indexes to optimize common query patterns.

| Index | Purpose |
|--------|---------|
| IX_Events_DomainName | Faster filtering by business domain. |
| IX_Events_CategoryName | Optimizes category-based searches. |
| IX_Speakers_SpeakerName | Speeds speaker lookups. |
| IX_Transcripts_EventId | Accelerates retrieval of transcripts for an event. |

---

# Typical Workflow

1. Create an event.
2. Register one or more speakers.
3. Associate speakers with the event.
4. Upload transcript files to external storage.
5. Store transcript metadata in SQL Server.
6. Retrieve metadata for downstream AI processing.

---

# AI Integration

The schema is designed as a metadata repository for AI applications.

Typical pipeline:

```text
Transcript File
      │
      ▼
Chunking
      │
      ▼
Embedding Generation
      │
      ▼
Qdrant Vector Database
      │
      ▼
Semantic Search
      │
      ▼
Recommendations / RAG
```

The relational database remains the source of truth for structured metadata, while vector databases store semantic embeddings.

---

# Design Decisions

- Asynchronous database access for scalability.
- Normalized schema to minimize redundancy.
- Separation of metadata from transcript content.
- Foreign key constraints maintain referential integrity.
- Indexed lookup columns improve query performance.
- Repository is designed to support AI-powered search and recommendation systems.

---
# Source Files

- `database/sql_server_client.py`
- `database/sql/event_tables.sql`
