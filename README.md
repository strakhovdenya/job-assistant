# 💼 AI Job Assistant

> Personal AI Job Search Operating System

A Python-based monorepo project designed to help you **collect, structure, analyze, and manage job opportunities** in a scalable and intelligent way.

---

## 🚀 Overview

This is not just a chatbot or a demo.

It is a **data-driven system** that evolves into a personal career assistant:

```
Job sources → Ingestion → Processing → Matching → Decision → Insights
```

The goal:

* centralize job opportunities
* evaluate fit automatically
* help make decisions (apply / skip / maybe)
* improve over time

---

## ✨ Features (Sprint 1)

### Backend (FastAPI)

* Job ingestion API
* Deduplication via SHA256 hash
* Pagination and sorting
* Clean layered architecture:

  * API → Services → Repositories → DB

### Frontend (Streamlit)

* Add job form
* Jobs list
* Job detail page

### Database

* PostgreSQL
* Structured models

---

## 🏗️ Project Structure

```
job-assistant/
├── apps/
│   ├── backend/      # FastAPI backend
│   └── frontend/     # Streamlit UI
├── packages/
│   └── shared/       # shared logic (future)
├── infra/
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

---

## 🧠 Architecture

* Backend: FastAPI + SQLAlchemy
* Frontend: Streamlit
* Database: PostgreSQL
* Dependency management: uv workspace

Principles:

* Modular monolith
* Data-first approach
* Human-in-the-loop
* Clear separation of concerns

---

## 📦 Tech Stack

* Python 3.12
* FastAPI
* SQLAlchemy 2.0
* Pydantic v2
* PostgreSQL
* Streamlit
* Docker
* uv (workspace)

---

## ⚙️ Setup

### 1. Clone repo

```bash
git clone https://github.com/strakhovdenya/job-assistant.git
cd job-assistant
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Run with Docker

```bash
docker compose up --build
```

---

## 🌐 Services

* Backend: http://localhost:8000
* API Docs: http://localhost:8000/docs
* Frontend: http://localhost:8501

---

## 🔌 API (Sprint 1)

### Health

```
GET /api/v1/health
```

### Create job

```
POST /api/v1/jobs/raw
```

### List jobs

```
GET /api/v1/jobs/raw
```

### Get job by ID

```
GET /api/v1/jobs/raw/{id}
```

---

## 📊 Data Models

### RawJob

* id
* raw_text
* source
* content_hash
* created_at

### Job (future use)

* id
* raw_job_id
* title
* company
* created_at

---

## 🧪 Example

```json
POST /api/v1/jobs/raw

{
  "raw_text": "Senior Python Developer, FastAPI, Remote",
  "source": "manual"
}
```

---

## 🛣️ Roadmap

### Sprint 2

* Parsing pipeline (RawJob → Job)
* LLM-based extraction
* Normalization

### Future

* Matching engine
* Recommendations (apply / skip)
* CV parsing
* RAG search
* Analytics
* AI agents

---

## 🧑‍💻 Development

Run backend locally:

```bash
uv run --package backend uvicorn app.main:app --reload
```

Run frontend locally:

```bash
uv run --package frontend streamlit run apps/frontend/app.py
```

---

## 🧩 Philosophy

1. Start simple
2. Add structure
3. Add intelligence
4. Add automation

---

## 🤝 Contributing

Contributions are welcome. Feel free to open issues or pull requests.

---

## 📄 License

MIT (or your preferred license)

