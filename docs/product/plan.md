# AI Job Assistant Project Plan

## Phase 1. Product Foundation
### Epic 1. Domain model and project skeleton
- Define entities: Job, RawJob, UserProfile, MatchResult, UserAction
- Define job lifecycle statuses
- Setup project structure (api, services, models, repositories, schemas)
- Configure .env and settings
- Setup FastAPI + Postgres
- Add logging and migrations

### Epic 2. Job data schema
- Define RawJob and Job schemas
- Define JobSkill entity
- Setup deduplication strategy
- Separate raw vs extracted fields

## Phase 2. Vacancy Ingestion
### Epic 3. Manual vacancy import
- Add endpoint/UI for manual input
- Save raw text
- Validate input

### Epic 4. Email ingestion
- Connect email source
- Parse emails
- Prevent duplicates

### Epic 5. Deduplication
- URL-based dedupe
- Text hash dedupe
- Soft dedupe logic

## Phase 3. Parsing and normalization
### Epic 6. Extraction pipeline
- Clean text
- Extract structured fields
- Validate and save

### Epic 7. Normalization
- Normalize seniority, skills, remote type, etc.

### Epic 8. Observability
- Logging
- Admin review UI
- Manual correction

## Phase 4. Job Workflow
### Epic 9. Inbox UI
- List view
- Filters
- Job detail view

### Epic 10. Decision workflow
- Apply / Maybe / Skip
- Store history and notes

## Phase 5. User Profile
### Epic 11. CV ingestion
- Upload CV
- Extract structured profile

### Epic 12. Preferences
- Preferred roles, stack, location, etc.

## Phase 6. Matching
### Epic 13. Scoring
- Skill, seniority, format matching

### Epic 14. Gap analysis
- Missing skills
- Strengths

### Epic 15. Recommendation
- Apply / Maybe / Skip logic

## Phase 7. Feedback Loop
### Epic 16. Human review
- Override system decisions

### Epic 17. Outcome tracking
- Track applications and results

## Phase 8. Retrieval
### Epic 18. Vector store
- Embeddings for jobs and profile

### Epic 19. Search API
- Keyword + semantic search

## Phase 9. RAG
### Epic 20. Job assistant
- Q&A over jobs

### Epic 21. Career docs
- CV, notes, templates

## Phase 10. Analytics
### Epic 22. Market insights
- Skills, trends

### Epic 23. Personal insights
- Skill gaps, behavior patterns

## Phase 11. Actions
### Epic 24. Application tools
- Cover letters
- CV adaptation

## Phase 12. Agents
### Epic 25. Agent orchestration
- Multi-agent system
