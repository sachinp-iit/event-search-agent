# Event Metadata Repository

## Overview

This repository contains the SQL Server database schema and asynchronous SQLAlchemy connectivity layer used to manage event metadata.

## Repository Contents

```
database/
├── sql_server_client.py
└── event_tables.sql
```

## Architecture

```text
Application
    │
    ▼
get_db_session()
    │
AsyncSession
    │
SQLAlchemy Async Engine
    │
SQL Server
```

## SQL Server Client

The `sql_server_client.py` module creates a singleton asynchronous SQLAlchemy engine and session factory.

### Features

- Async SQLAlchemy engine
- Connection pooling
- Connection health checks (`pool_pre_ping`)
- Dependency Injection ready session provider
- Session reuse using `async_sessionmaker`

### Engine Configuration

```python
_engine = create_async_engine(
    settings.SQL_SERVER_CONNECTION_STRING,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
```

### Session Lifecycle

```text
Request
  │
  ▼
get_db_session()
  │
Create AsyncSession
  │
Yield Session
  │
Execute Queries
  │
Session Closed Automatically
```

## Database Schema

The attached SQL file defines the SQL Server schema used by the application.

```sql
-- ===========================================================================================================
-- database/sql/event_tables.sql
-- ===========================================================================================================
-- SQL Server Database Schema
--
-- Purpose:
-- - Event Metadata Repository
-- - Transcript Metadata Repository
-- - Speaker Relationships
-- - QDrant Payload Enrichment Layer
-- - Recommendation Engine Foundation
-- ===========================================================================================================


-- ===========================================================================================================
-- EVENTS
-- ===========================================================================================================
CREATE TABLE Events (
    EventId BIGINT IDENTITY(1,1) PRIMARY KEY,
    EventName VARCHAR(500) NOT NULL,
    EventTopic VARCHAR(150) NOT NULL,
    EventAgenda VARCHAR(MAX) NULL,
    DomainName VARCHAR(75) NULL,
    CategoryName VARCHAR(75) NULL,
    EventStartDate DATETIME NOT NULL,
    EventEndDate DATETIME NOT NULL,
    AuthorName VARCHAR(75) NULL,
    EventCompany VARCHAR(75) NULL,
    EventLocation VARCHAR(100) NULL,
    CreatedAt DateTime DEFAULT GETUTCDATE(),
    UpdatedAt DateTime NULL
);

GO

-- ===========================================================================================================
-- SPEAKERS
-- ===========================================================================================================
CREATE TABLE Speakers (
    SpeakerId BIGINT IDENTITY(1,1) PRIMARY KEY,
    SpeakerName VARCHAR(75) NOT NULL,
    SpeakerTitle VARCHAR(75) NULL,
    SpeakerCompany VARCHAR(75) NULL,
    CreatedAt DateTime DEFAULT GETUTCDATE()
);

GO

-- ===========================================================================================================
-- EVENT SPEAKERS
-- ===========================================================================================================
CREATE TABLE EventSpeakers (
    EventSpeakerId BIGINT IDENTITY(1,1) PRIMARY KEY,
    EventId BIGINT NOT NULL,
    SpeakerId BIGINT NOT NULL,
    FOREIGN KEY (EventId) REFERENCES Events(EventId),
    FOREIGN KEY (SpeakerId) REFERENCES Speakers(SpeakerId),
    CreatedAt DateTime DEFAULT GETUTCDATE()
);

GO

-- ===========================================================================================================
-- EVENT SPEAKERS
-- ===========================================================================================================
CREATE TABLE Transcripts (
    TranscriptId BIGINT IDENTITY(1,1) PRIMARY KEY,
    EventId BIGINT NULL,
    TranscriptLocation VARCHAR(2000) NOT NULL,
    TranscriptFileName VARCHAR(1000) NOT NULL,
    TranscriptVersion INT DEFAULT 1,
    IsAutoModerated BIT DEFAULT 0,
    CreatedAt DateTime DEFAULT GETUTCDATE()
    FOREIGN KEY (EventId) REFERENCES Events(EventId)
);

GO

-- ===========================================================================================================
-- INDEXES
-- ===========================================================================================================
CREATE INDEX IX_Events_DomainName ON Events(DomainName);

GO

CREATE INDEX IX_Events_CategoryName ON Events(CategoryName);

GO

CREATE INDEX IX_Speakers_SpeakerName ON Speakers(SpeakerName);

GO

CREATE INDEX IX_Transcripts_EventId ON Transcripts(EventId);

```

## Python Source

```python
# database/sql_server_client.py

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from config.settings import settings

from collections.abc import AsyncGenerator


# =========================================================
# SQL SERVER ENGINE
# =========================================================

_engine = create_async_engine (
    settings.SQL_SERVER_CONNECTION_STRING,
    pool_pre_ping = True,
    pool_size = 10,
    max_overflow = 20
)


# =========================================================
# SESSION FACTORY
# =========================================================
_session_factory = async_sessionmaker (
    bind = _engine,
    expire_on_commit = False,
    class_ = AsyncSession
)


# =========================================================
# SESSION PROVIDER
# =========================================================
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async SQL Server session provider.
    """
    
    async with _session_factory() as session:
        yield session
```

## Design

- Uses asynchronous database access.
- Connection pooling improves throughput.
- Sessions are scoped using async context managers.
- Configuration is externalized through application settings.

## Future Improvements

- ORM models
- Repository layer
- Migration scripts
- Unit tests
