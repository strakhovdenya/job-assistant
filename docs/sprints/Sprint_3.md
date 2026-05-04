# 🚀 Sprint 3 — AI Assistant (Draft → Review → Save)

## 🎯 Цель спринта

Добавить AI Assistant для структуризации вакансии:

```text
RawJob → AI draft → user review → save Job
```

### Главный принцип

AI не сохраняет Job напрямую.  
AI создаёт черновик, пользователь проверяет, редактирует и только потом сохраняет Job.

---

## 🧠 Контекст

Sprint 1 дал:

- монорепу
- backend
- frontend
- PostgreSQL
- RawJob ingestion
- базовый UI flow

Sprint 2 дал:

- RawJob → Job flow
- Job Editor
- редактируемые skills
- backend CRUD
- frontend tests
- ручную структуризацию вакансий

Sprint 3 добавляет AI-помощника поверх существующего ручного flow.

---

## 🧠 Главный инсайт

Sprint 2:

```text
RawJob → manual structuring → Job
```

Sprint 3:

```text
RawJob → AI draft → user review/edit → Job
```

AI ускоряет заполнение формы, но не становится источником истины.

---

## 🏗️ Архитектура

### Поток данных

```text
RawJob
  ↓
AI Extraction Pipeline
  ↓
JobDraft
  ↓
User Review
  ↓
Job
```

### Новая сущность

Добавляется `JobDraft`.

```text
RawJob     — исходный неизменяемый текст
JobDraft   — AI-черновик, который можно редактировать
Job        — финальная структурированная вакансия
```

---

## 🧩 Pipeline вместо полноценного graph

В Sprint 3 не внедряем LangGraph или другой orchestration framework.

Вместо этого делаем простой pipeline шагов:

```python
pipeline = [
    CleanTextStep(),
    DetectLanguageStep(),
    ExtractStructuredDataStep(),
    NormalizeFieldsStep(),
    ValidateResultStep(),
]
```

Это даёт graph-ready архитектуру без overengineering.

Позже pipeline можно заменить на graph runner, не переписывая бизнес-логику шагов.

---

# 🧱 Backlog Sprint 3

---

## 🧱 Epic 1 — Domain Model: JobDraft

- [x] Создать backend model `JobDraft`
- [x] Добавить связь `JobDraft.raw_job_id → RawJob.id`
- [x] Добавить поле `title`
- [x] Добавить поле `company`
- [x] Добавить поле `location`
- [x] Добавить поле `language`
- [x] Добавить поле `seniority`
- [x] Добавить поле `remote_type`
- [x] Добавить поле `employment_type`
- [x] Добавить поле `skills`
- [x] Добавить поле `description`
- [x] Добавить поле `ai_model`
- [x] Добавить поле `ai_confidence`
- [x] Добавить поле `ai_warnings`
- [x] Добавить поле `extraction_status`
- [x] Добавить `created_at`
- [x] Добавить `updated_at`
- [x] Создать Alembic migration
- [x] Проверить migration upgrade
- [ ] Проверить migration downgrade

### `extraction_status`

```text
draft
failed
reviewed
saved
```

### DoD

- [x] Таблица `job_drafts` создаётся
- [x] JobDraft связан с RawJob
- [ ] Draft можно сохранить в БД
- [ ] Draft можно прочитать из БД

---

## 🧱 Epic 2 — RawJob Processing Status

- [x] Добавить новый статус `ai_drafted`
- [x] Обновить allowed statuses для `RawJob.processing_status`
- [ ] При создании AI draft выставлять `processing_status = ai_drafted`
- [ ] При сохранении draft как Job выставлять `processing_status = structured`
- [ ] Проверить, что RawJob.raw_text не изменяется

### Итоговый lifecycle

```text
raw → reviewed → ai_drafted → structured
```

### DoD

- [ ] RawJob получает статус `ai_drafted` после AI draft
- [ ] RawJob получает статус `structured` после сохранения Job
- [ ] RawJob остаётся source of truth

---

## 🧱 Epic 3 — Pydantic Schemas

- [x] Создать `app/schemas/job_draft.py`
- [x] Создать `JobDraftResponse`
- [x] Создать `JobDraftUpdate`
- [x] Создать `JobDraftCreate`
- [x] Создать `AIExtractionResult`
- [x] Создать `AIExtractionError`
- [x] Добавить validation для `skills`
- [x] Добавить validation для `confidence`
- [x] Добавить validation для enum-like полей
- [x] Extra fields игнорируются или безопасно обрабатываются

### AI output schema

```json
{
  "title": null,
  "company": null,
  "location": null,
  "language": null,
  "seniority": null,
  "remote_type": null,
  "employment_type": null,
  "skills": [],
  "description": null,
  "confidence": 0.0,
  "warnings": []
}
```

### DoD

- [x] AI response валидируется через Pydantic
- [x] Missing fields принимаются как `null`
- [x] Некорректный AI response не ломает backend
- [x] Extra fields игнорируются или безопасно обрабатываются

---

## 🧱 Epic 4 — AI Client

- [ ] Создать `app/services/ai/ai_client.py`
- [ ] Добавить интерфейс `AIClient`
- [ ] Добавить `extract_job(raw_text: str)`
- [ ] Добавить timeout
- [ ] Добавить retry 1 раз
- [ ] Добавить JSON-only parsing
- [ ] Добавить обработку invalid JSON
- [ ] Добавить обработку timeout
- [ ] Добавить обработку provider error
- [ ] Добавить fake AI client для тестов

### Env config

```env
AI_ENABLED=true
AI_PROVIDER=openai_compatible
AI_BASE_URL=
AI_API_KEY=
AI_MODEL=
AI_TIMEOUT_SECONDS=30
```

### DoD

- [ ] AI client изолирован от бизнес-логики
- [ ] Тесты могут использовать FakeAIClient
- [ ] Реальный AI не вызывается в unit tests
- [ ] Ошибки AI возвращаются контролируемо

---

## 🧱 Epic 5 — Prompt Design

- [ ] Создать `app/services/ai/prompts.py`
- [ ] Описать system prompt
- [ ] Описать user prompt template
- [ ] Требовать JSON-only response
- [ ] Запретить AI выдумывать отсутствующие данные
- [ ] Если поле не найдено, возвращать `null`
- [ ] Skills извлекать только из текста вакансии
- [ ] Добавлять warnings при неуверенности
- [ ] Ограничить description кратким summary

### Prompt rules

```text
- Do not invent company name.
- Do not invent salary.
- If field is missing, return null.
- Return valid JSON only.
- Extract skills only if mentioned or strongly implied.
- Keep description short.
```

### DoD

- [ ] Prompt возвращает стабильный JSON contract
- [ ] Prompt не смешан с API route
- [ ] Prompt можно тестировать отдельно

---

## 🧱 Epic 6 — Extraction Pipeline

- [ ] Создать `app/services/ai/pipeline.py`
- [ ] Создать `PipelineContext`
- [ ] Создать base class/interface для step
- [ ] Реализовать `CleanTextStep`
- [ ] Реализовать `DetectLanguageStep`
- [ ] Реализовать `ExtractStructuredDataStep`
- [ ] Реализовать `NormalizeFieldsStep`
- [ ] Реализовать `ValidateResultStep`
- [ ] Реализовать `JobExtractionPipeline`
- [ ] Добавить warnings/errors в context
- [ ] Добавить unit tests для каждого step

### PipelineContext

```python
class PipelineContext:
    raw_text: str
    cleaned_text: str | None
    language: str | None
    extracted_data: dict | None
    normalized_data: dict | None
    warnings: list[str]
    errors: list[str]
```

### DoD

- [ ] Pipeline запускается по RawJob
- [ ] Каждый step тестируется отдельно
- [ ] AI вызов находится только в `ExtractStructuredDataStep`
- [ ] Pipeline можно расширить без переписывания service

---

## 🧱 Epic 7 — JobDraft Repository

- [ ] Создать `app/repositories/job_draft_repository.py`
- [ ] Реализовать `create`
- [ ] Реализовать `get_by_id`
- [ ] Реализовать `update`
- [ ] Реализовать `list_by_raw_job`
- [ ] Реализовать проверку существования draft
- [ ] Добавить tests repository layer

### DoD

- [ ] Draft создаётся
- [ ] Draft читается
- [ ] Draft обновляется
- [ ] Draft можно получить по RawJob

---

## 🧱 Epic 8 — Job Extraction Service

- [ ] Создать `app/services/job_extraction_service.py`
- [ ] Реализовать `create_draft_from_raw(raw_job_id)`
- [ ] Реализовать `regenerate_draft(raw_job_id)`
- [ ] Подключить pipeline
- [ ] Сохранять результат pipeline как JobDraft
- [ ] Обрабатывать RawJob not found
- [ ] Обрабатывать AI failure
- [ ] Обновлять RawJob processing_status
- [ ] Не создавать Job автоматически

### DoD

- [ ] RawJob превращается в JobDraft
- [ ] AI failure не создаёт Job
- [ ] Ошибка возвращается понятно
- [ ] RawJob.raw_text не изменяется

---

## 🧱 Epic 9 — Draft → Job Service

- [ ] Расширить `job_service.py`
- [ ] Реализовать `create_job_from_draft(draft_id)`
- [ ] Перенести поля из JobDraft в Job
- [ ] Установить `skills_source = ai`
- [ ] Если пользователь менял skills, установить `skills_source = mixed`
- [ ] Обновить `JobDraft.extraction_status = saved`
- [ ] Обновить `RawJob.processing_status = structured`
- [ ] Защититься от повторного save одного draft

### DoD

- [ ] Draft можно сохранить как Job
- [ ] Повторный save не создаёт duplicate Job
- [ ] Job отображается в существующем Jobs List
- [ ] Статусы обновляются корректно

---

## 🧱 Epic 10 — API Endpoints

- [ ] Создать или расширить routes для draft flow
- [ ] Реализовать `POST /api/v1/jobs/raw/{raw_job_id}/ai-draft`
- [ ] Реализовать `GET /api/v1/jobs/drafts/{draft_id}`
- [ ] Реализовать `PATCH /api/v1/jobs/drafts/{draft_id}`
- [ ] Реализовать `POST /api/v1/jobs/drafts/{draft_id}/save`
- [ ] Опционально: `GET /api/v1/jobs/raw/{raw_job_id}/drafts`
- [ ] Подключить router в `main.py`
- [ ] Добавить обработку 404
- [ ] Добавить обработку AI errors
- [ ] Добавить API tests

### DoD

- [ ] Все endpoints работают
- [ ] Ошибки возвращаются в понятном формате
- [ ] API не сохраняет Job без явного save
- [ ] Integration tests проходят

---

## 🧱 Epic 11 — Frontend API Client

- [ ] Добавить `generate_ai_draft(raw_job_id)`
- [ ] Добавить `get_job_draft(draft_id)`
- [ ] Добавить `update_job_draft(draft_id, payload)`
- [ ] Добавить `save_draft_as_job(draft_id)`
- [ ] Добавить обработку loading
- [ ] Добавить обработку errors
- [ ] Добавить tests для client methods

### DoD

- [ ] Frontend умеет работать с draft API
- [ ] Ошибки backend отображаются корректно
- [ ] Старый Job flow не сломан

---

## 🧱 Epic 12 — Raw Jobs UI

- [ ] Добавить кнопку `Generate AI Draft`
- [ ] Добавить loading state
- [ ] Добавить success state
- [ ] Добавить error state
- [ ] После генерации открывать Draft Editor
- [ ] Если draft уже существует, дать возможность открыть его
- [ ] Добавить кнопку `Regenerate Draft` только если это безопасно

### DoD

- [ ] Пользователь может запустить AI draft из RawJob
- [ ] UI не зависает во время AI вызова
- [ ] Ошибка AI видна пользователю
- [ ] Existing manual flow остаётся рабочим

---

## 🧱 Epic 13 — AI Draft Editor UI

- [ ] Создать страницу `job_draft_edit.py`
- [ ] Загрузить draft по id
- [ ] Показать `title`
- [ ] Показать `company`
- [ ] Показать `location`
- [ ] Показать `language`
- [ ] Показать `seniority`
- [ ] Показать `remote_type`
- [ ] Показать `employment_type`
- [ ] Показать `description`
- [ ] Показать skills editor
- [ ] Показать raw_text в expander
- [ ] Показать AI warnings
- [ ] Показать AI confidence
- [ ] Добавить кнопку `Save Draft`
- [ ] Добавить кнопку `Save as Job`
- [ ] Добавить кнопку `Regenerate Draft`

### DoD

- [ ] Draft можно открыть
- [ ] Все поля можно отредактировать
- [ ] Skills можно добавить и удалить
- [ ] Draft можно сохранить
- [ ] Draft можно сохранить как Job

---

## 🧱 Epic 14 — Skills Source Logic

- [ ] Draft skills по умолчанию считаются AI-generated
- [ ] Если пользователь не менял skills, сохранять `skills_source = ai`
- [ ] Если пользователь менял skills, сохранять `skills_source = mixed`
- [ ] Не вводить сложные категории skills
- [ ] Не вводить веса skills

### DoD

- [ ] Skills остаются простым `list[str]`
- [ ] Источник skills сохраняется корректно
- [ ] Skills editor работает как в Sprint 2

---

## 🧱 Epic 15 — Backend Tests

- [ ] Unit test: CleanTextStep
- [ ] Unit test: DetectLanguageStep
- [ ] Unit test: NormalizeFieldsStep
- [ ] Unit test: ValidateResultStep
- [ ] Unit test: AI response validation
- [ ] Unit test: invalid JSON
- [ ] Unit test: timeout handling
- [ ] Unit test: draft creation
- [ ] Unit test: draft update
- [ ] Unit test: draft save as Job
- [ ] Integration test: POST ai-draft
- [ ] Integration test: GET draft
- [ ] Integration test: PATCH draft
- [ ] Integration test: POST draft save
- [ ] Test: save draft twice does not duplicate Job
- [ ] Test: failed AI call does not create Job

### DoD

- [ ] Backend tests проходят
- [ ] Real AI не вызывается в tests
- [ ] Edge cases покрыты

---

## 🧱 Epic 16 — Frontend Tests

- [ ] Test: Generate AI Draft button visible
- [ ] Test: loading state
- [ ] Test: error state
- [ ] Test: Draft Editor opens
- [ ] Test: fields prefilled
- [ ] Test: user can edit fields
- [ ] Test: user can edit skills
- [ ] Test: Save Draft
- [ ] Test: Save as Job
- [ ] Test: Job appears in Jobs List

### DoD

- [ ] Frontend tests проходят
- [ ] Старые Sprint 2 tests не сломаны
- [ ] UI flow покрыт

---

## 🧱 Epic 17 — End-to-End Flow

- [ ] Создать RawJob
- [ ] Открыть RawJob
- [ ] Нажать `Generate AI Draft`
- [ ] Получить AI draft
- [ ] Открыть Draft Editor
- [ ] Проверить prefilled поля
- [ ] Исправить title
- [ ] Исправить company
- [ ] Добавить skill
- [ ] Удалить лишний skill
- [ ] Сохранить Draft
- [ ] Сохранить Draft как Job
- [ ] Проверить Jobs List
- [ ] Проверить RawJob status
- [ ] Проверить Job detail

### DoD

- [ ] Полный пользовательский flow работает
- [ ] Данные сохраняются
- [ ] Ошибки отображаются
- [ ] RawJob остаётся неизменным

---

# 🎯 Sprint 3 Definition of Done

Спринт завершён, если:

- [ ] Можно открыть RawJob
- [ ] Можно сгенерировать AI draft
- [ ] Draft сохраняется отдельно от Job
- [ ] Draft можно редактировать
- [ ] Skills можно редактировать
- [ ] Draft можно сохранить как Job
- [ ] Job отображается в Jobs List
- [ ] RawJob остаётся неизменным
- [ ] RawJob получает корректный processing_status
- [ ] AI ошибки не ломают backend
- [ ] AI ошибки не ломают frontend
- [ ] Backend tests проходят
- [ ] Frontend tests проходят
- [ ] Real AI не используется в tests
- [ ] Pipeline реализован
- [ ] Graph framework не добавлен

---

# 🔄 Рекомендуемый порядок реализации

## Step 1 — Schemas and Models

- [ ] JobDraft model
- [ ] JobDraft schemas
- [ ] AI schemas
- [ ] Migration

## Step 2 — AI Client

- [ ] FakeAIClient
- [ ] Real AIClient
- [ ] Config
- [ ] Error handling

## Step 3 — Pipeline

- [ ] Context
- [ ] Steps
- [ ] Runner
- [ ] Unit tests

## Step 4 — Backend Services

- [ ] JobDraft repository
- [ ] JobExtractionService
- [ ] Draft → Job save logic

## Step 5 — API

- [ ] Draft endpoints
- [ ] Error handling
- [ ] Integration tests

## Step 6 — Frontend Client

- [ ] Draft API methods
- [ ] Loading/error handling

## Step 7 — UI

- [ ] RawJob generate button
- [ ] Draft Editor
- [ ] Skills editor reuse
- [ ] Save as Job flow

## Step 8 — E2E

- [ ] Full manual scenario
- [ ] Regression check Sprint 2 flow

---

# 🚫 What NOT to do in Sprint 3

- [ ] Не делать matching engine
- [ ] Не делать CV parsing
- [ ] Не делать embeddings
- [ ] Не делать pgvector
- [ ] Не делать RAG
- [ ] Не делать semantic search
- [ ] Не делать LangGraph
- [ ] Не делать multi-agent orchestration
- [ ] Не делать email ingestion
- [ ] Не делать cover letters
- [ ] Не делать auto-apply
- [ ] Не делать auto-save AI result as Job
- [ ] Не делать сложную taxonomy skills
- [ ] Не делать skill weights
- [ ] Не делать scoring по вакансии
- [ ] Не делать user profile

---

# 📦 Deliverable

В конце Sprint 3 должно быть:

- backend AI draft flow
- persisted JobDraft
- AI extraction pipeline
- AI client abstraction
- fake AI client for tests
- draft API endpoints
- frontend draft editor
- RawJob → AI draft → review → Job flow
- tests

---

# 🚀 Next Sprint Preview

Sprint 4 может быть посвящён:

- улучшению normalization
- качеству extraction
- user profile foundation
- подготовке к matching MVP
