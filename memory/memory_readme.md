# Conversation Memory Module

## Overview

The **Memory** module is responsible for maintaining conversational context across user interactions. It provides a lightweight in-memory session store, prompt formatting utilities, and an LLM-powered summarization component to help applications remain within model context limits while preserving important information.

The module is divided into four independent components:

| Component | Responsibility |
|-----------|----------------|
| `ConversationMemory` | Stores conversation history for a single session. |
| `MemoryManager` | Manages memory instances for multiple sessions. |
| `MemoryPromptHelper` | Converts conversation history into prompt-ready context. |
| `ConversationSummarizer` | Compresses older conversations into concise summaries using an LLM. |

---

# High-Level Architecture

![Transcript Search Memory Architecture](https://github.com/sachinp-iit/event-search-agent/blob/main/assets/Transcript%20Search%20Agent-Memory%20Module%20Architecture.png)

---

# Component Details

## 1. ConversationMemory

### Purpose

`ConversationMemory` is the core storage component for a single conversation. It maintains an ordered collection of user and assistant messages and automatically limits history size.

### Internal Design

The class uses Python's `collections.deque` with a configurable `maxlen`, ensuring that older messages are automatically discarded once the configured history limit is reached.

### Responsibilities

- Store conversation history.
- Preserve message order.
- Automatically evict old messages.
- Provide history retrieval.
- Support complete memory reset.

### Public Methods

#### `add_message(role, content)`

Adds a message object containing the sender role and message content.

#### `get_history()`

Returns the complete conversation as a list of dictionaries.

#### `clear()`

Removes every stored message for the conversation.

### Design Benefits

- Constant-time append operations.
- Automatic memory management.
- No manual cleanup required.
- Predictable memory usage.

---

## 2. MemoryManager

### Purpose

`MemoryManager` acts as the session registry for the application.

Instead of creating memory objects throughout the application, every component requests memory from this manager using a unique session identifier.

### Responsibilities

- Create conversation memory on demand.
- Maintain one memory object per session.
- Remove inactive sessions.
- Clear every active session when required.

### Session Lifecycle

```text
Session ID
     │
     ▼
Exists?
 │        │
No        Yes
 │         │
Create     Return Existing
 │
 ▼
ConversationMemory
```

### Advantages

- Prevents duplicate memory creation.
- Supports concurrent users.
- Centralized memory ownership.
- Simple session cleanup.

---

## 3. MemoryPromptHelper

### Purpose

Large Language Models require conversation history to be formatted before being inserted into prompts.

This helper converts structured memory into prompt-friendly representations.

### Responsibilities

- Restrict context length.
- Select only the latest messages.
- Convert structured history into readable text.

### Processing Flow

```text
ConversationMemory
        │
        ▼
Retrieve History
        │
        ▼
Trim to Maximum Messages
        │
        ▼
Format
(USER: ...)
(ASSISTANT: ...)
        │
        ▼
Prompt Context
```

### Methods

#### `build_context()`

Returns only the most recent messages, preventing prompt overflow.

#### `build_text()`

Formats history as plain text suitable for prompt injection.

Example:

```text
USER: What events happened last week?

ASSISTANT: Here are the recent events...
```

### Benefits

- Smaller prompts.
- Lower token consumption.
- Improved model performance.
- Cleaner prompt formatting.

---

## 4. ConversationSummarizer

### Purpose

As conversations grow, they may exceed the language model's context window.

The summarizer compresses older interactions into a concise summary while preserving important information.

### Architecture

```text
Conversation History
        │
        ▼
Prompt Construction
        │
        ▼
Language Model
        │
        ▼
String Output Parser
        │
        ▼
Conversation Summary
```

### Summary Strategy

The summarization prompt instructs the model to retain:

- Important entities
- Event names
- Speaker names
- Company names
- User intent
- Outstanding questions

This ensures future prompts preserve context without resending the entire conversation.

### Benefits

- Reduces token usage.
- Prevents context overflow.
- Retains critical business information.
- Enables long-running conversations.

---

# Overall Memory Flow

```text
User Message
      │
      ▼
MemoryManager
      │
      ▼
ConversationMemory
      │
      ├────────► MemoryPromptHelper
      │                │
      │                ▼
      │        Prompt Context
      │
      └────────► ConversationSummarizer
                       │
                       ▼
               Compressed Summary
```

---

# Design Principles

- Separation of concerns.
- Single responsibility for each component.
- Configurable history limits.
- Session-based memory isolation.
- Efficient in-memory storage.
- Prompt optimization for LLMs.
- Extensible architecture for persistent storage (Redis, SQL, etc.).

---
