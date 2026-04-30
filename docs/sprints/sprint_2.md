# 🚀 Спринт 2 — Manual Structuring + AI-Ready Foundation

## 🎯 Цель спринта

Построить надёжный слой структурированных данных, где:

- пользователь вручную превращает RawJob в Job  
- система готова к будущей интеграции AI  
- данные становятся пригодными для анализа и будущего matching  

RawJob → ручная структуризация → Job → (в будущем AI-помощник)

---

## 🧠 Главный принцип

Sprint 2 — не про автоматический парсинг.

Sprint 2 — про:
- управляемые данные  
- ручную структуризацию  
- подготовку под AI  

---

## ⚠️ Ключевые ограничения

### ❌ НЕ делаем
- OpenAI / LLM интеграцию
- автоматический парсинг как источник истины
- сложную модель skills (категории, веса и т.д.)
- сложную extraction-логику

### ✅ Делаем
- ручную структуризацию
- редактируемые поля
- простую модель skills
- UI для редактирования
- основу для AI

---

# 🧱 Задачи спринта

---

## 1. Обновление модели Job

Добавить поля:

title: str | None  
company: str | None  
location: str | None  
language: str | None  
seniority: str | None  
remote_type: str | None  
employment_type: str | None  
status: str  

skills: list[str]  

description: str | None  
notes: str | None  

skills_source: str  # manual / ai / mixed  

created_at  
updated_at  

Принцип: максимально просто, без переусложнения.

---

## 2. Связь RawJob → Job

raw_job_id: int

- каждый Job связан с RawJob  
- RawJob остаётся неизменным  
- RawJob = source of truth  

---

## 3. Статус обработки

Добавить в RawJob:

processing_status: str

Значения:

raw → reviewed → structured

---

## 4. API для Job

Добавить эндпоинты:

POST   /api/v1/jobs/from-raw/{raw_job_id}  
GET    /api/v1/jobs  
GET    /api/v1/jobs/{id}  
PATCH  /api/v1/jobs/{id}  

---

## 5. Работа со skills (упрощённо)

### Модель:

skills: list[str]  
skills_source: str  

### Поведение:

- пользователь вводит вручную  
- можно добавлять / удалять  
- без категорий и сложной логики  

### Важно:

skills — это AI-задача в будущем, но сейчас:
- источник истины = пользователь  
- AI будет только помогать  

---

## 6. Минимальные подсказки (опционально)

Можно добавить:

- определение языка (ru / en / de)  
- определение seniority (junior / middle / senior)  
- определение remote  

Но:

Это только подсказки, не логика системы.

---

## 7. UI (Streamlit)

### 📄 Страница: Raw Jobs Review

Функции:

- отображение raw_text  
- кнопка: Create Job  

---

### 📄 Страница: Job Editor

Форма:

- title  
- company  
- location  
- seniority  
- remote_type  
- language  
- status  
- notes  

---

### 📄 Skills Editor

- поле ввода  
- кнопка "Add"  
- список skills  
- удаление  

---

### 📄 Jobs List

Отображает:

- title  
- company  
- status  
- дата  

---

## 8. Поток работы пользователя

1. Пользователь добавляет RawJob  
2. Открывает его  
3. Нажимает "Create Job"  
4. Заполняет поля  
5. Добавляет skills  
6. Сохраняет  
7. Видит Job в списке  

---

## 🔄 Поток данных

RawJob  
↓  
User review  
↓  
Manual structuring  
↓  
Job  
↓  
Future: AI enrichment  

---

## 📦 Результат спринта

К концу спринта:

- есть таблица Job  
- есть ручная структуризация  
- skills редактируются  
- UI позволяет редактировать  
- RawJob остаётся неизменным  
- система готова к AI  

---

## 🎯 Definition of Done

Спринт завершён, если:

1. Можно открыть RawJob  
2. Можно создать Job  
3. Можно заполнить:
   - title  
   - company  
4. Можно добавить skills  
5. Можно сохранить  
6. Job отображается в списке  

---

## 💡 Ключевой инсайт

Сначала делаем данные управляемыми → потом делаем их умными

---

## 🚀 Следующий спринт (Sprint 3)

- интеграция OpenAI  
- AI extraction (skills, title и др.)  
- draft → review → save  
- начало matching engine  

---

## 🧠 Архитектурная логика

Sprint 1 → ingestion  
Sprint 2 → manual structuring
- updated_at поддерживается на уровне приложения (SQLAlchemy), без DB triggers на этом этапе

Sprint 3 → AI assistance  

---

## 🧩 Почему это правильный подход

Проблема:

- вакансии разные  
- языки разные  
- структура нестабильная  

Решение:

- человек = источник истины  
- AI = помощник  

---

## 🧠 Итог

Sprint 2 — это фундамент всей системы.

Без него невозможно:
- matching  
- рекомендации  
- аналитика  
- AI  

Этот спринт превращает проект из “хранилища текста” в “систему данных”.

---

# 📋 Backlog (разбивка задач Sprint 2)

## 🧱 Epic 1 — Domain Model

- [x] Обновить модель `Job` (app/models/job.py):
  - [x] title
  - [x] company
  - [x] location
  - [x] language
  - [x] seniority
  - [x] remote_type
  - [x] employment_type
  - [x] status
  - [x] skills (list[str] / JSON)
  - [x] skills_source
  - [x] description
  - [x] notes
  - [x] updated_at

- [x] Обновить Pydantic схемы (app/schemas/job.py):
  - [x] JobResponse
  - [x] JobUpdate

- [x] Добавить связь `raw_job_id` → RawJob

---

- [x] Добавить `processing_status` в `RawJob` (app/models/raw_job.py):
  - [x] значения: raw / reviewed / structured

---

- [x] Создать и применить миграции:
  - [x] alembic revision
  - [x] alembic upgrade head
  - [x] проверить rollback

---

## 🧱 Epic 2 — Backend (Repository + Service)

- [x] Создать job_repository.py:
  - [x] create_from_raw
  - [x] get_by_id
  - [x] list
  - [x] update

- [x] Создать job_service.py:
  - [x] create_job_from_raw(raw_job_id)
  - [x] update_job(job_id, data)
  - [x] list_jobs()
  - [x] get_job(job_id)

- [x] Бизнес-логика:
- [x] при создании Job обновлять RawJob.processing_status = structured

---

## 🧱 Epic 3 — API

- [x] Создать `routes_jobs.py`

- [x] Реализовать endpoints:
  - [x] POST   /api/v1/jobs/from-raw/{raw_job_id}
  - [x] GET    /api/v1/jobs
  - [x] GET    /api/v1/jobs/{id}
  - [x] PATCH  /api/v1/jobs/{id}

- [x] Валидация:
  - [x] проверка существования RawJob
  - [x] проверка существования Job
  - [x] обработка ошибок

- [x] Подключить роутер в main.py

---

## 🧱 Epic 4 — Skills (MVP)

- [ ] Добавить поддержку `skills` в Job:
  - [ ] хранение list[str]
  - [ ] обновление через PATCH

- [ ] Реализовать:
  - [ ] добавление skills
  - [ ] удаление skills
  - [ ] перезапись списка

---

## 🧱 Epic 5 — Streamlit UI

### Raw Jobs Review

- [ ] Создать страницу:
  - apps/frontend/pages/1_Raw_Jobs.py

- [ ] Реализовать:
  - [ ] список RawJob
  - [ ] кнопка "Create Job"

---

### Job Editor

- [ ] Создать страницу:
  - apps/frontend/pages/2_Job_Editor.py

- [ ] Реализовать форму:
  - [ ] title
  - [ ] company
  - [ ] location
  - [ ] seniority
  - [ ] remote_type
  - [ ] language
  - [ ] status
  - [ ] notes

---

### Skills UI

- [ ] поле ввода
- [ ] кнопка Add
- [ ] список skills
- [ ] удаление

---

### Jobs List

- [ ] Создать страницу:
  - apps/frontend/pages/3_Jobs.py

- [ ] Отобразить:
  - [ ] title
  - [ ] company
  - [ ] status
  - [ ] created_at

---

### API Client

- [ ] Добавить методы:
  - [ ] create_job_from_raw
  - [ ] update_job
  - [ ] list_jobs
  - [ ] get_job

---

## 🧱 Epic 6 — Подсказки (optional)

- [ ] detect_language()
- [ ] detect_seniority()
- [ ] detect_remote()

👉 Используются только как default значения

---

## 🧱 Epic 7 — End-to-End Flow

- [ ] Проверить полный сценарий:
  - [ ] создать RawJob
  - [ ] открыть его
  - [ ] создать Job
  - [ ] заполнить поля
  - [ ] добавить skills
  - [ ] сохранить
  - [ ] увидеть в списке

- [ ] Проверить:
  - [ ] данные сохраняются
  - [ ] ошибки обрабатываются
  - [ ] RawJob не изменяется

---

## 🎯 Итоговый Definition of Done

- [ ] можно открыть RawJob  
- [ ] можно создать Job  
- [ ] можно заполнить title и company  
- [ ] можно добавить skills  
- [ ] можно сохранить Job  
- [ ] Job отображается в списке  
- [ ] RawJob остаётся неизменным  

---