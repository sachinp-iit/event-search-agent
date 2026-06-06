# Configuration Layer

## Overview

The Configuration Layer acts as the central control center of the application. It is responsible for managing all environment-specific settings, external service configurations, model parameters, and operational controls from a single location.

Instead of hardcoding values throughout the codebase, the application loads configuration from environment variables and exposes them through a centralized settings module. This approach improves maintainability, security, and deployment flexibility.

---

## Files

```text
.env
config/
└── settings.py
```

---

## Purpose

The Configuration Layer provides a centralized mechanism for managing application settings and infrastructure configurations.

### Key Objectives

- Centralize all configuration values
- Keep secrets outside source code
- Support multiple deployment environments
- Simplify application maintenance
- Enable configuration-driven architecture
- Improve security and scalability

Without this layer, configuration values would be scattered across multiple modules, making updates difficult and increasing operational risks.

---

## Architecture

```text
.env
   │
   ▼
config/settings.py
   │
   ├── OpenRouter Settings
   ├── Qdrant Settings
   ├── Embedding Settings
   ├── LangSmith/Langfuse Settings
   └── Ingestion Settings
```

The `.env` file stores environment-specific values while `settings.py` loads, validates, and exposes them to the rest of the application.

---

# Environment Configuration (`.env`)

## Description

The `.env` file contains all runtime configuration values required by the application.

These values can vary between Development, Testing, Staging, and Production environments without requiring code modifications.

---

# Settings Management (`config/settings.py`)

## Description

The `settings.py` module acts as the centralized configuration loader.

It reads values from environment variables and exposes them through strongly typed configuration objects that can be used throughout the application.

---

# OpenRouter Configuration

## Purpose

OpenRouter configuration manages all settings related to Large Language Model (LLM) communication.

---

# Qdrant Configuration

## Purpose

Qdrant configuration controls how the application connects to the vector database.

---

# Embedding Model Configuration

## Purpose

Embedding configuration determines which embedding model converts text into vector representations.

---

# LangSmith / Langfuse Configuration

## Purpose

Observability and tracing configuration enables monitoring and debugging of LLM workflows.

---

# Ingestion Configuration

## Purpose

Ingestion configuration controls transcript processing behavior including chunk size, overlap, batching, and indexing parameters.
