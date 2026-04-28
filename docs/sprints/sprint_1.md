# Sprint 1 — Backlog (Monorepo + Docker, Updated Structure)

## Goal
Build a **production-like monorepo foundation** with:
- backend (FastAPI)
- frontend (Next.js)
- PostgreSQL
- Docker-based local environment
- first end-to-end flow (UI → API → DB)

---

## Final Project Structure

```text
job-assistant/
  apps/
    backend/
      app/
      alembic/
      Dockerfile
    frontend/
      app/
      Dockerfile
  packages/
    shared/
  infra/
    compose/
    scripts/
  docker-compose.yml
  .env.example
  Makefile
```

---

## Sprint Scope
- monorepo bootstrap
- docker environment
- backend skeleton
- frontend skeleton
- DB setup
- raw job ingestion
- minimal UI integration

---

# Tasks

## 1. Monorepo Bootstrap

- [ ] Create folders:
  - apps/backend
  - apps/frontend
  - packages/shared
  - infra/compose
  - infra/scripts
- [ ] Add root files:
  - docker-compose.yml
  - .env.example
  - Makefile
  - README.md

**DoD:**
- Repo structure matches target layout
- Project can be cloned and started consistently

---

## 2. Docker Environment

- [ ] Create docker-compose.yml
- [ ] Add services:
  - backend
  - frontend
  - postgres
- [ ] Configure network
- [ ] Add DB volume
- [ ] Setup env variables
- [ ] Add basic healthchecks

**DoD:**
- docker compose up запускает все сервисы
- backend и frontend доступны
- postgres сохраняет данные

---

## 3. Backend Setup (apps/backend)

- [ ] Init FastAPI project
- [ ] Create structure:
  - app/api
  - app/core
  - app/models
  - app/schemas
  - app/services
  - app/repositories
  - app/db
- [ ] Add config (env-based)
- [ ] Setup logging
- [ ] Add `/api/v1/health` endpoint

**DoD:**
- Backend запускается в Docker
- Health endpoint работает
- Конфиг читается из env

---

## 4. Database Setup

- [ ] Connect PostgreSQL
- [ ] Setup SQLAlchemy
- [ ] Setup Alembic (apps/backend/alembic)
- [ ] Create initial migration
- [ ] Create tables:
  - jobs_raw
  - jobs

**DoD:**
- Миграции применяются
- Таблицы создаются
- Backend читает/пишет в БД

---

## 5. Domain Models

- [ ] Define RawJob model:
  - id
  - raw_text
  - source
  - content_hash
  - created_at
- [ ] Define Job model:
  - id
  - raw_job_id
  - title
  - company
  - created_at
- [ ] Setup relationships

**DoD:**
- ORM модели соответствуют БД
- CRUD операции работают

---

## 6. Backend API (Raw Jobs)

### Ingestion
- [ ] POST /api/v1/jobs/raw
- [ ] Validate input
- [ ] Generate hash
- [ ] Save to DB

### Retrieval
- [ ] GET /api/v1/jobs/raw
- [ ] Pagination
- [ ] Sorting

- [ ] GET /api/v1/jobs/raw/{id}

**DoD:**
- Можно добавить вакансию
- Можно получить список
- Можно получить одну вакансию

---

## 7. Deduplication v1

- [ ] Add content_hash logic
- [ ] Check duplicates before insert
- [ ] Return existing record if duplicate

**DoD:**
- Дубликаты не создаются
- Поведение предсказуемо

---

## 8. Frontend Setup (apps/frontend)

- [ ] Init Next.js
- [ ] Create base layout
- [ ] Add pages:
  - Jobs list
  - Add job form
- [ ] Configure API URL
- [ ] Run in Docker

**DoD:**
- Frontend запускается
- Страницы доступны

---

## 9. Frontend ↔ Backend Integration

- [ ] Form → POST raw job
- [ ] Fetch jobs list
- [ ] Display jobs
- [ ] Handle loading/errors

**DoD:**
- Пользователь может добавить вакансию через UI
- Она появляется в списке
- Полный flow работает

---

## 10. Shared Package

- [ ] Create packages/shared
- [ ] Add constants:
  - job statuses
  - sources
- [ ] Define contract strategy (optional v1)

**DoD:**
- Shared пакет существует
- Есть базовые константы

---

## Dependencies

- Bootstrap → everything
- Docker → all apps
- Backend → DB
- DB → Models
- Models → API
- API → Frontend integration

---

## Deliverable

В конце спринта:

- монорепа с правильной структурой
- docker-compose окружение
- backend (FastAPI)
- frontend (Next.js)
- postgres
- ingestion API
- retrieval API
- UI для добавления вакансий
- дедупликация
- end-to-end flow

---

## What NOT to do

- No RAG
- No embeddings
- No LangGraph
- No CV parsing
- No matching logic

Фокус: **инфраструктура + первый вертикальный срез**

---

## Next Sprint (Preview)

Sprint 2:
- parsing pipeline
- extraction (LLM)
- normalization
- переход RawJob → Job
