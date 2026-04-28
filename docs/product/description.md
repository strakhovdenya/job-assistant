# Personal AI Job Assistant — Project Description

## Overview

This project is a **Personal AI Job Search Operating System**.

It is not just a chatbot or a RAG demo. It is a system that:
- collects job opportunities,
- structures and analyzes them,
- compares them to your profile,
- helps you make decisions,
- and continuously improves based on your behavior.

---

## Core Idea

Pipeline:

**Job sources → Ingestion → Normalization → Matching → Decision → Actions → History → Insights**

The system evolves from a simple inbox into a personalized career assistant.

---

## Key Value

### Immediate Value
- Centralized job inbox
- Deduplication of вакансий
- Быстрое понимание “подходит / не подходит”
- Сохранение решений

### Advanced Value
- Анализ рынка по твоим вакансиям
- Персональные рекомендации
- Генерация откликов
- AI-assisted decision making

---

## Functional Blocks

### 1. Job Ingestion
- Import from email
- Manual input
- URL parsing (future)

### 2. Data Storage
- Raw job data
- Structured job data
- User profile
- Actions and history

### 3. Parsing & Normalization
- Extract structured fields:
  - title
  - company
  - location
  - skills
  - seniority
- Normalize data:
  - skill names
  - remote format
  - job types

### 4. Job Inbox
- List of jobs
- Filters and sorting
- Status management:
  - new
  - maybe
  - applied
  - skipped

### 5. User Profile
- CV upload
- Skill extraction
- Preferences:
  - roles
  - stack
  - location
  - salary

### 6. Matching Engine
- Compare job ↔ profile
- Fit score calculation
- Breakdown:
  - skills
  - seniority
  - preferences

### 7. Recommendation System
- Suggest:
  - APPLY
  - MAYBE
  - SKIP
- Provide explanations

### 8. Feedback Loop
- Track user decisions
- Track outcomes:
  - interview
  - rejection
  - offer
- Improve recommendations

### 9. Retrieval (RAG Layer)
- Semantic search over jobs
- Search over CV and notes
- Natural language queries

### 10. Analytics
- Skill demand trends
- Gap analysis
- Market insights
- Personal performance insights

### 11. Application Support
- Generate cover letters
- Adapt CV
- Generate summaries

### 12. Agent Layer (Future)
- Ingestion agent
- Matching agent
- Decision agent
- Analytics agent

---

## Architecture Principles

- Data-first, not RAG-first
- Modular monolith
- Clear domain separation:
  - ingestion
  - processing
  - matching
  - retrieval
  - analytics
- Human-in-the-loop
- Observability and traceability

---

## Technology Stack (Recommended)

- Backend: FastAPI (Python)
- Database: PostgreSQL
- Vector DB: pgvector / Chroma
- LLM: OpenAI / compatible
- UI: Web UI or Telegram bot

---

## Development Philosophy

1. Start with simple working system
2. Add structure
3. Add intelligence
4. Add retrieval
5. Add automation
6. Add agents

---

## MVP Definition

The first working version includes:

- Job ingestion
- Structured job data
- CV parsing
- Matching score
- Recommendation (apply/maybe/skip)
- Basic UI

---

## Long-term Vision

A fully personalized AI assistant that:

- understands your career goals,
- tracks your job search,
- analyzes market trends,
- helps you make better decisions,
- and improves over time.

