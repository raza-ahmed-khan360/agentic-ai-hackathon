# RAG Backend Constitution

## Core Principles

### I. API Compliance and Standardization
All API endpoints must follow REST conventions with proper HTTP methods, status codes, and request/response schemas.

### II. Vector Database Integration
All document ingestion and retrieval must use Qdrant as the single source of truth for embeddings and semantic search.

### III. AI Model Compatibility
All AI interactions must use Google Gemini 2.5 Flash via OpenAI-compatible endpoints for consistency and cost efficiency.

### IV. Environment Security
All sensitive credentials (API keys, URLs) must be stored in `.env` file and never hardcoded in source code.

### V. Code Quality and Testing
All endpoints must have proper error handling, logging, and input validation using Pydantic models.

### VI. Documentation and Traceability
All feature implementations must be documented in specs/ and tracked through Prompt History Records (PHRs).

## Governance

This Constitution is the single source of truth for backend development standards. All contributions and reviews must verify compliance.

**Version**: 1.0.0 | **Created**: 2025-11-30 | **Last Amended**: 2025-11-30
