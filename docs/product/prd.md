# Personal AI Job Assistant — Product Requirements Document (PRD)

## 1. Product Overview

### Vision
Build a **Personal AI Job Search Operating System** that helps users:
- collect job opportunities
- evaluate fit
- make decisions
- track outcomes
- improve job search strategy over time

### Core Concept
Pipeline:
**Sources → Ingestion → Processing → Matching → Decision → Actions → Insights**

---

## 2. Goals

### Primary Goals
- Reduce time spent reviewing irrelevant вакансии
- Improve decision quality (apply vs skip)
- Provide visibility into skill gaps
- Build personal job market intelligence

### Success Metrics (MVP)
- % of jobs reviewed via system
- Time saved per job decision
- Accuracy of match recommendations (user agreement rate)
- Number of jobs processed

---

## 3. Users

### Target User
- Individual job seeker (initially you)
- Tech-focused roles

---

## 4. Functional Scope

### 4.1 Ingestion
- Manual job input
- Email ingestion (future)

### 4.2 Processing
- Raw job storage
- Structured extraction
- Normalization
- Deduplication

### 4.3 Job Inbox
- Job list UI
- Filters & sorting
- Status management

### 4.4 User Profile
- CV upload
- Skill extraction
- Preferences (role, stack, location)

### 4.5 Matching Engine
- Fit score
- Skill comparison
- Gap analysis

### 4.6 Decision System
- Apply / Maybe / Skip
- Explanation

### 4.7 Feedback Loop
- Track decisions
- Track outcomes

### 4.8 Retrieval (Post-MVP)
- Semantic search
- RAG Q&A

### 4.9 Analytics (Post-MVP)
- Skill demand
- Personal gaps

---

## 5. Non-Goals (MVP)
- Full automation of job applications
- Multi-agent orchestration
- Multi-source scraping

---

## 6. Architecture

### Approach
- Modular monolith
- Data-first architecture
- Human-in-the-loop

### Components
- Ingestion service
- Processing pipeline
- Matching engine
- API layer
- Storage layer

---

## 7. Tech Stack

- Backend: FastAPI
- Database: PostgreSQL
- Vector DB: pgvector (later)
- LLM: OpenAI-compatible API
- UI: Web UI

---

## 8. Roadmap

### Release 0.1 — Job Inbox
- Manual ingestion
- Deduplication
- Job list UI
- Status management

### Release 0.2 — Structured Jobs
- Extraction pipeline
- Normalization

### Release 0.3 — Matching MVP
- CV ingestion
- Match scoring
- Recommendation

### Release 0.4 — RAG Layer
- Vector search
- Job Q&A

### Release 0.5 — Analytics
- Market insights
- Personal insights

### Release 0.6 — Agents
- Workflow automation

---

## 9. MVP Definition

Must include:
- Job ingestion
- Structured data
- CV parsing
- Matching score
- Recommendation
- Basic UI

---

## 10. Risks

- Overengineering too early
- Poor data quality from extraction
- Lack of real dataset early

Mitigation:
- Start simple
- Use manual review
- Iterate on real data

---

## 11. Development Strategy

1. Build data layer
2. Build processing pipeline
3. Add matching
4. Add retrieval
5. Add analytics
6. Add automation

---

## 12. Future Vision

A system that:
- learns from user behavior
- adapts recommendations
- provides strategic career insights
