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
