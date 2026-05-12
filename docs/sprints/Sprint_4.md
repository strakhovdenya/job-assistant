# 🚀 Sprint 4 — Stabilize AI Draft Flow + Profile Foundation + Matching Readiness

## 🎯 Цель спринта

Сделать систему пригодной для следующего шага — **Matching MVP**.

Sprint 4 не должен начинаться с нового большого функционала. Он начинается с закрытия незавершённого Sprint 3, потому что без стабильного flow:

```text
RawJob → AI Draft → User Review/Edit → Structured Job
```

нельзя качественно строить matching, рекомендации и профиль пользователя.

К концу Sprint 4 система должна иметь:

```text
RawJob
  → AI Draft
  → Reviewed Structured Job
  → Normalized Job Data
  → User Profile + Preferences
  → Ready for Matching MVP
```

---

## 🧠 Контекст

Sprint 1 дал:

- монорепу
- backend
- frontend
- PostgreSQL
- Docker
- RawJob ingestion
- дедупликацию
- первый UI/API flow

Sprint 2 дал:

- RawJob → Job flow
- ручную структуризацию вакансий
- Job Editor
- редактируемые skills
- backend CRUD
- frontend flow
- ручной fallback для структуризации

Sprint 3 добавил AI-помощника:

```text
RawJob → AI Draft → User Review/Edit → Job
```

Но Sprint 3 не был закрыт полностью по Definition of Done. Остались незавершённые части:

- корректные статусы `RawJob.processing_status`
- корректные статусы `JobDraft.extraction_status`
- frontend draft API client
- завершение Draft Editor
- raw_text в Draft Editor
- regenerate draft из Draft Editor
- skills_source logic
- E2E flow
- часть frontend/backend tests
- regression check старого manual flow

Product roadmap после Structured Jobs ведёт к Release 0.3 — Matching MVP:

- CV / Profile ingestion
- match scoring
- recommendation

Но переходить к matching до стабилизации structured jobs нельзя.

---

## 🧠 Главный принцип Sprint 4

Sprint 4 — не про то, чтобы начать сразу много новых направлений.

Sprint 4 — про то, чтобы пройти реальную последовательность:

```text
1. Закрыть AI Draft flow
2. Проверить полный пользовательский путь
3. Нормализовать данные вакансий
4. Добавить User Profile foundation
5. Добавить Preferences foundation
6. Подготовить контракт для Matching MVP
```

Каждый следующий блок начинается только после того, как предыдущий работает end-to-end.

---

## 🚫 Что было неправильно в Sprint 3

В Sprint 3 план был построен по эпикам, но фактическая работа пошла вразброс:

- часть backend была сделана глубже, чем требовалось
- часть frontend осталась недоделанной
- часть статусов была реализована непоследовательно
- были расхождения в naming: `saved` / `accepted`, `ai` / `ai_reviewed`
- E2E flow не был доведён до состояния “можно пользоваться”
- некоторые задачи были отмечены как частично сделанные, но не закрывали пользовательский сценарий целиком

В Sprint 4 стратегия другая:

```text
Не закрываем эпики ради галочек.
Закрываем пользовательские потоки в правильном порядке.
```

---

## 🟢 С чего начинается Sprint 4

Sprint 4 начинается не с User Profile и не с Matching.

Он начинается с **Sprint 3 Stabilization Gate**:

```text
RawJob → Generate AI Draft → Edit Draft → Save Draft → Save as Job → Job appears in Jobs List
```

Пока этот flow не работает полностью, новый функционал не добавляется.

---

## 🔴 Чем заканчивается Sprint 4

Sprint 4 заканчивается не полноценным matching engine.

Sprint 4 заканчивается состоянием:

```text
- у нас есть стабильные structured jobs
- у нас есть нормализованные поля вакансии
- у нас есть user profile draft
- у нас есть preferences
- у нас есть контракт MatchResult
- у нас есть данные, на которых можно делать scoring в Sprint 5
```

То есть Sprint 4 — это последний подготовительный спринт перед настоящим Matching MVP.

---

# 📦 Sprint Scope

## ✅ Входит в Sprint 4

- закрытие незавершённых задач Sprint 3
- корректные статусы `RawJob` и `JobDraft`
- стабильный AI Draft UI flow
- frontend API client для draft flow
- E2E проверка RawJob → Job
- normalization v1
- UserProfile model
- UserPreferences model
- ручной ввод профиля и preferences
- подготовка контрактов для будущего matching
- тесты и regression check Sprint 1–3 flow

## ❌ Не входит в Sprint 4

- полноценный matching score
- recommendation APPLY / MAYBE / SKIP
- CV file upload parser
- embeddings
- RAG
- pgvector
- analytics
- agents
- email ingestion
- cover letters
- auto-apply
- сложные веса skills
- сложная taxonomy skills
- fake scoring

---

# 🏗️ Архитектурная логика

## До Sprint 4

```text
RawJob
  ↓
Manual structuring / AI Draft
  ↓
Job
```

## После Sprint 4

```text
RawJob
  ↓
AI Draft / Manual Review
  ↓
Structured Job
  ↓
Normalized Job

UserProfile
UserPreferences

Normalized Job + UserProfile + UserPreferences
  ↓
Ready for Matching MVP
```

---

# 🧱 Backlog Sprint 4

---

## 🧱 Epic 1 — Sprint 3 Stabilization: AI Draft Flow

### 🎯 Цель

Закрыть незавершённый Sprint 3 и сделать AI Draft flow рабочим от начала до конца.

### 🧩 Tasks

- [ ] Проверить, что `JobDraft` можно создать из `RawJob`
- [ ] Проверить, что `JobDraft` сохраняется отдельно от `Job`
- [ ] Проверить, что `JobDraft` можно прочитать из БД
- [ ] Проверить, что `JobDraft` можно редактировать
- [ ] Проверить, что `skills` можно редактировать в draft
- [ ] Проверить, что draft можно сохранить как `Job`
- [ ] Проверить, что `Job` появляется в Jobs List
- [ ] Проверить, что `RawJob.raw_text` остаётся неизменным
- [ ] Проверить, что повторный save draft не создаёт duplicate Job
- [ ] Проверить, что AI failure не создаёт Job
- [ ] Проверить, что старый manual flow из Sprint 2 не сломан

### ✅ DoD

- [ ] Полный AI Draft flow работает вручную
- [ ] Полный AI Draft flow покрыт тестами
- [ ] Backend не создаёт Job без явного user action
- [ ] Старый manual flow из Sprint 2 не сломан
- [ ] RawJob остаётся source of truth

---

## 🧱 Epic 2 — Processing Status Cleanup

### 🎯 Цель

Привести lifecycle в понятное и предсказуемое состояние.

В Sprint 3 остались незакрытые вопросы по:

- `RawJob.processing_status`
- `JobDraft.extraction_status`
- `skills_source`
- несоответствию `saved` / `accepted`
- несоответствию `ai` / `ai_reviewed`

Это нужно закрыть до Matching MVP.

### Финальный lifecycle RawJob

```text
raw
  → ai_drafted
  → structured

raw
  → failed
```

### Финальный lifecycle JobDraft

```text
draft
  → reviewed
  → saved

draft
  → failed
```

### 🧩 Tasks

- [ ] При создании AI Draft выставлять `RawJob.processing_status = ai_drafted`
- [ ] При сохранении draft как Job выставлять `RawJob.processing_status = structured`
- [ ] При AI failure выставлять контролируемый статус / ошибку
- [ ] Унифицировать `JobDraft.extraction_status`
- [ ] Заменить расхождение `accepted` / `saved`
- [ ] Запретить некорректные переходы статусов
- [ ] Проверить, что Job не может существовать при некорректном RawJob lifecycle
- [ ] Добавить tests на lifecycle

### ✅ DoD

- [ ] Статусы обновляются одинаково в backend, API и UI
- [ ] Нет ситуации, где Job создан, а RawJob остался `ai_drafted`
- [ ] Нет ситуации, где Draft сохранён как Job, но Draft не помечен как `saved`
- [ ] Ошибки AI не ломают lifecycle
- [ ] Lifecycle понятен для будущего matching

---

## 🧱 Epic 3 — Frontend Draft API Client

### 🎯 Цель

Закрыть незавершённый frontend слой из Sprint 3.

Draft operations не должны быть размазаны по UI. Все операции должны идти через единый API client.

### 🧩 Tasks

- [ ] Добавить `generate_ai_draft(raw_job_id)`
- [ ] Добавить `get_job_draft(draft_id)`
- [ ] Добавить `update_job_draft(draft_id, payload)`
- [ ] Добавить `save_draft_as_job(draft_id)`
- [ ] Добавить `regenerate_ai_draft(raw_job_id)`
- [ ] Унифицировать обработку backend errors
- [ ] Унифицировать loading state
- [ ] Добавить frontend tests для client methods
- [ ] Проверить, что старые API client methods из Sprint 2 работают

### ✅ DoD

- [ ] UI не вызывает draft API напрямую вразнобой
- [ ] Все draft operations идут через один client layer
- [ ] Ошибки backend отображаются пользователю
- [ ] Loading state отображается пользователю
- [ ] Manual RawJob → Job flow не сломан

---

## 🧱 Epic 4 — AI Draft Editor Completion

### 🎯 Цель

Довести Draft Editor до рабочего состояния, а не до “почти готов”.

### 🧩 Tasks

- [ ] Показать `RawJob.raw_text` в expander
- [ ] Добавить кнопку `Regenerate Draft`
- [ ] Проверить редактирование всех полей:
  - [ ] title
  - [ ] company
  - [ ] location
  - [ ] language
  - [ ] seniority
  - [ ] remote_type
  - [ ] employment_type
  - [ ] description
- [ ] Проверить добавление skills
- [ ] Проверить удаление skills
- [ ] Проверить `Save Draft`
- [ ] Проверить `Save as Job`
- [ ] После `Save as Job` вести пользователя в Job detail / Jobs List
- [ ] Показывать AI warnings понятно
- [ ] Показывать AI confidence понятно
- [ ] Не скрывать от пользователя, что AI мог ошибиться

### ✅ DoD

- [ ] Draft можно открыть
- [ ] Draft можно отредактировать
- [ ] Draft можно сохранить
- [ ] Draft можно пересгенерировать
- [ ] Draft можно сохранить как Job
- [ ] Пользователь видит raw source при ревью
- [ ] UI поддерживает human-in-the-loop принцип

---

## 🧱 Epic 5 — Skills Source Logic

### 🎯 Цель

Сделать понятное происхождение skills.

В Sprint 2 skills были ручными. В Sprint 3 появились AI-generated skills. В Sprint 4 нужно явно сохранить источник данных.

### Rules

```text
manual — skills введены пользователем вручную
ai     — skills пришли из AI draft и не менялись
mixed  — AI skills были изменены пользователем
```

### 🧩 Tasks

- [ ] При manual Job сохранять `skills_source = manual`
- [ ] При save draft без изменения skills сохранять `skills_source = ai`
- [ ] При изменении draft skills сохранять `skills_source = mixed`
- [ ] Убрать / заменить `ai_reviewed`, если он уже используется
- [ ] Не добавлять веса skills
- [ ] Не добавлять категории skills
- [ ] Не добавлять skill taxonomy
- [ ] Добавить tests

### ✅ DoD

- [ ] Источник skills сохраняется корректно
- [ ] Skills остаются простым `list[str]`
- [ ] Логика пригодна для будущего matching
- [ ] UI не усложняется
- [ ] Существующие jobs не ломаются из-за изменения значения `skills_source`

---

# 🧱 Epic 6 — Normalization v1: AI-assisted enums + deterministic cleanup

## 🎯 Цель

Сделать structured jobs пригодными для будущего matching.

Matching не должен каждый раз разбирать произвольный текст и значения вроде:

```text
remote / Remote / fully remote / удалёнка / Home office
senior / Senior / sr / lead-ish
full-time / fulltime / full time
```

Для этого нужен простой normalization layer, но в Sprint 4 мы **не делаем отдельный AI normalization pipeline** и **не делаем отдельный AI-вызов после draft**.

Вместо этого используем гибридный подход:

```text
AI Extraction Prompt
  → JobDraft with enum-like values
  → User Review/Edit
  → NormalizationService
  → Structured Job
```

Главный принцип:

```text
AI понимает контекст.
NormalizationService гарантирует стабильный системный формат.
```

---

## 🧠 Стратегия normalization в Sprint 4

### 1. AI возвращает значения в разрешённом формате

На уровне AI extraction prompt нужно явно требовать, чтобы модель возвращала только допустимые значения для enum-like полей.

AI должен не просто извлечь текстовое значение, а привести его к системному значению.

Например:

```text
"Home office" → remote
"fully remote" → remote
"2 days office / 3 days remote" → hybrid
"Vollzeit" → full_time
"Senior Backend Engineer" → senior
"Werkstudent" → internship или unknown, если контекст неясен
```

Если AI не уверен — возвращает:

```text
unknown
```

Это означает, что основное контекстное понимание происходит на этапе:

```text
RawJob → AI Draft
```

А не отдельным normalization-запросом позже.

---

### 2. NormalizationService не вызывает AI

`normalization_service.py` в Sprint 4 — это не второй AI-слой.

Он не должен повторно анализировать вакансию и не должен делать отдельный LLM call.

Его задача:

```text
принять значение → привести к допустимому enum → если значение непонятно, вернуть unknown
```

Пример:

```text
Remote → remote
remote work → remote
fully_remote → remote
home office → remote
hybrid work → hybrid
on-site → onsite
sr → senior
senior-level → senior
fulltime → full_time
full-time → full_time
непонятное значение → unknown
```

То есть `NormalizationService` — это deterministic cleanup и safety layer, а не интеллектуальный парсер.

---

### 3. Skills нормализуются только базово

Для skills в Sprint 4 не делаем taxonomy, категории, веса или отдельную AI-нормализацию.

Делаем только базовую очистку:

```text
trim
remove duplicates
canonical readable form
preserve readable values
```

Пример:

```text
[" Python ", "python", "FastAPI", "fast api"]
```

можно привести к:

```text
["Python", "FastAPI"]
```

Но не нужно превращать это в сложную модель вроде:

```text
FastAPI → Python Backend Framework
PostgreSQL → Database
React.js → Frontend Framework
```

Это не scope Sprint 4.

---

## Поля для normalization v1

```text
language
seniority
remote_type
employment_type
skills
```

---

## Target values

### language

```text
en
de
ru
unknown
```

### seniority

```text
junior
middle
senior
lead
unknown
```

### remote_type

```text
remote
hybrid
onsite
unknown
```

### employment_type

```text
full_time
part_time
contract
internship
unknown
```

---

## 🧩 Tasks

### Prompt / AI extraction contract

- [ ] Обновить AI extraction prompt
- [ ] Явно указать allowed values для `language`
- [ ] Явно указать allowed values для `seniority`
- [ ] Явно указать allowed values для `remote_type`
- [ ] Явно указать allowed values для `employment_type`
- [ ] Добавить правило: если значение не найдено или AI не уверен — вернуть `unknown`
- [ ] Добавить правило: не возвращать произвольные значения вне enum
- [ ] Добавить правило: не выдумывать значения, которых нет в вакансии
- [ ] Добавить prompt examples:
  - [ ] `Home office` → `remote`
  - [ ] `fully remote` → `remote`
  - [ ] `2 days office` → `hybrid`
  - [ ] `Vollzeit` → `full_time`
  - [ ] `fulltime` → `full_time`
  - [ ] `sr` / `Senior` → `senior`
  - [ ] `Tech Lead` / `Team Lead` → `lead`

---

### Backend normalization layer

- [ ] Создать `normalization_service.py`
- [ ] Реализовать `normalize_language(value)`
- [ ] Реализовать `normalize_seniority(value)`
- [ ] Реализовать `normalize_remote_type(value)`
- [ ] Реализовать `normalize_employment_type(value)`
- [ ] Реализовать `normalize_skills(skills)`
- [ ] Добавить deterministic mapping для частых вариантов
- [ ] Все неизвестные значения приводить к `unknown`
- [ ] Не делать отдельный AI call внутри normalization service
- [ ] Не делать сложный regex engine
- [ ] Не делать skill taxonomy
- [ ] Не добавлять skill weights

---

### Integration

- [ ] Подключить normalization при `save Draft as Job`
- [ ] Подключить normalization при manual `Job` update
- [ ] Проверить, что normalization не портит ручные данные
- [ ] Проверить, что `RawJob.raw_text` остаётся неизменным
- [ ] Проверить, что пользователь всё ещё может исправить значения вручную
- [ ] Проверить, что после ручного исправления данные сохраняются в допустимом формате

---

### Tests

- [ ] Добавить unit tests для `normalize_language`
- [ ] Добавить unit tests для `normalize_seniority`
- [ ] Добавить unit tests для `normalize_remote_type`
- [ ] Добавить unit tests для `normalize_employment_type`
- [ ] Добавить unit tests для `normalize_skills`
- [ ] Добавить tests на unknown fallback
- [ ] Добавить tests, что normalization не вызывает AI
- [ ] Добавить tests на save Draft as Job with normalization
- [ ] Добавить tests на manual Job update with normalization

---

## ✅ DoD

- [ ] AI extraction prompt возвращает enum-like значения
- [ ] JobDraft получает значения, близкие к системному формату
- [ ] `NormalizationService` не вызывает AI
- [ ] `NormalizationService` приводит значения к допустимым target values
- [ ] Все неизвестные значения безопасно превращаются в `unknown`
- [ ] Job после сохранения имеет предсказуемые normalized fields
- [ ] Matching в Sprint 5 сможет использовать эти поля без парсинга на лету
- [ ] Normalization не ломает ручные данные
- [ ] Skills остаются простым `list[str]`
- [ ] Нет skill taxonomy
- [ ] Нет skill weights
- [ ] RawJob остаётся неизменным
- [ ] Normalization покрыта unit tests

---

## 🚫 Что НЕ делаем в Epic 6

- [ ] Не делаем отдельный AI normalization call
- [ ] Не добавляем второй LLM pipeline после draft
- [ ] Не добавляем LangGraph / orchestration
- [ ] Не строим большую regex-систему
- [ ] Не делаем taxonomy skills
- [ ] Не добавляем веса skills
- [ ] Не делаем matching score
- [ ] Не делаем recommendation logic

---

## 🧠 Итоговая формула

```text
AI Draft отвечает за контекстное понимание.
NormalizationService отвечает за стабильность данных.
```

Sprint 4 не должен усложнять AI-архитектуру, но должен гарантировать, что в `Job` попадут значения, пригодные для Matching MVP в Sprint 5.

## 🧱 Epic 7 — User Profile Foundation

### 🎯 Цель

Добавить базовую сущность пользователя для будущего matching.

В Sprint 4 не делаем полноценный CV parser. Вместо этого делаем ручной profile foundation, чтобы Sprint 5 мог строить matching.

### Model: UserProfile

```text
id
full_name
target_roles: list[str]
skills: list[str]
seniority
locations: list[str]
languages: list[str]
created_at
updated_at
```

### 🧩 Backend tasks

- [ ] Создать model `UserProfile`
- [ ] Создать schemas:
  - [ ] `UserProfileCreate`
  - [ ] `UserProfileUpdate`
  - [ ] `UserProfileResponse`
- [ ] Создать Alembic migration
- [ ] Создать repository
- [ ] Создать service
- [ ] Создать API:
  - [ ] `GET /api/v1/profile`
  - [ ] `PUT /api/v1/profile`
- [ ] Добавить backend tests

### 🧩 Frontend tasks

- [ ] Добавить страницу `Profile`
- [ ] Добавить редактирование `full_name`
- [ ] Добавить редактирование `skills`
- [ ] Добавить редактирование `target_roles`
- [ ] Добавить редактирование `seniority`
- [ ] Добавить редактирование `locations`
- [ ] Добавить редактирование `languages`
- [ ] Добавить save/load state
- [ ] Добавить error state
- [ ] Добавить frontend tests

### ✅ DoD

- [ ] Пользователь может создать / обновить профиль
- [ ] Skills профиля редактируются
- [ ] Target roles редактируются
- [ ] Профиль сохраняется в БД
- [ ] Профиль можно получить через API
- [ ] Профиль можно отредактировать через UI
- [ ] Нет CV parsing в этом спринте

---

## 🧱 Epic 8 — Preferences Foundation

### 🎯 Цель

Отделить “кто я” от “что я ищу”.

Profile отвечает за опыт и навыки. Preferences отвечают за желаемую работу.

Это нужно для будущих рекомендаций APPLY / MAYBE / SKIP.

### Model: UserPreferences

```text
id
preferred_roles: list[str]
preferred_locations: list[str]
remote_preference
employment_types: list[str]
preferred_languages: list[str]
must_have_skills: list[str]
nice_to_have_skills: list[str]
excluded_keywords: list[str]
created_at
updated_at
```

### 🧩 Backend tasks

- [ ] Создать model `UserPreferences`
- [ ] Создать schemas:
  - [ ] `UserPreferencesCreate`
  - [ ] `UserPreferencesUpdate`
  - [ ] `UserPreferencesResponse`
- [ ] Создать migration
- [ ] Создать repository
- [ ] Создать service
- [ ] Создать API:
  - [ ] `GET /api/v1/preferences`
  - [ ] `PUT /api/v1/preferences`
- [ ] Добавить backend tests

### 🧩 Frontend tasks

- [ ] Добавить UI секцию на странице Profile или отдельную страницу Preferences
- [ ] Добавить редактирование `preferred_roles`
- [ ] Добавить редактирование `preferred_locations`
- [ ] Добавить редактирование `remote_preference`
- [ ] Добавить редактирование `employment_types`
- [ ] Добавить редактирование `preferred_languages`
- [ ] Добавить редактирование `must_have_skills`
- [ ] Добавить редактирование `nice_to_have_skills`
- [ ] Добавить редактирование `excluded_keywords`
- [ ] Добавить save/load state
- [ ] Добавить error state
- [ ] Добавить frontend tests

### ✅ DoD

- [ ] Preferences сохраняются отдельно от UserProfile
- [ ] Можно задать preferred roles
- [ ] Можно задать remote preference
- [ ] Можно задать must-have / nice-to-have skills
- [ ] Можно задать excluded keywords
- [ ] Данные готовы для scoring в Sprint 5

---

## 🧱 Epic 9 — Matching Contract Preparation

### 🎯 Цель

Подготовить контракт matching, но не реализовывать полноценный scoring.

В Sprint 4 мы готовим структуру, чтобы в Sprint 5 не спорить о форме результата.

### Draft contract

```json
{
  "job_id": 1,
  "profile_id": 1,
  "score": null,
  "recommendation": null,
  "breakdown": {
    "skills": {
      "matched": [],
      "missing": []
    },
    "seniority": {
      "job": null,
      "profile": null,
      "status": null
    },
    "preferences": {
      "matched": [],
      "conflicts": []
    }
  },
  "explanation": null
}
```

### 🧩 Tasks

- [ ] Создать `MatchResult` schema
- [ ] Создать `MatchBreakdown` schema
- [ ] Создать `SkillMatchBreakdown`
- [ ] Создать `SeniorityMatchBreakdown`
- [ ] Создать `PreferenceMatchBreakdown`
- [ ] Добавить validation для `recommendation`
- [ ] Добавить validation для `score`
- [ ] Не сохранять MatchResult в БД в Sprint 4, если это не нужно
- [ ] Добавить unit tests на schema validation
- [ ] Задокументировать будущий endpoint:
  - [ ] `POST /api/v1/jobs/{job_id}/match`

### ✅ DoD

- [ ] Есть согласованный контракт MatchResult
- [ ] Matching в Sprint 5 можно делать без изменения Job/Profile моделей
- [ ] Нет fake scoring
- [ ] Нет recommendation logic в Sprint 4
- [ ] Нет преждевременной таблицы match_results без необходимости

---

## 🧱 Epic 10 — Regression & E2E

### 🎯 Цель

Проверить, что Sprint 4 не сломал Sprint 1–3.

### Flow A — RawJob ingestion

```text
Add RawJob → RawJob appears in list → RawJob detail opens
```

- [ ] Создать RawJob через UI
- [ ] Проверить, что RawJob появился в списке
- [ ] Открыть RawJob detail
- [ ] Проверить, что raw_text сохранён
- [ ] Проверить deduplication behavior

### Flow B — Manual structuring

```text
RawJob → Create Job manually → Edit fields → Edit skills → Save → Job appears in Jobs List
```

- [ ] Открыть RawJob
- [ ] Нажать Create Job
- [ ] Заполнить title
- [ ] Заполнить company
- [ ] Добавить skills
- [ ] Сохранить Job
- [ ] Проверить Jobs List
- [ ] Проверить Job detail

### Flow C — AI draft structuring

```text
RawJob → Generate AI Draft → Edit Draft → Save Draft → Save as Job → Job appears in Jobs List
```

- [ ] Открыть RawJob
- [ ] Нажать Generate AI Draft
- [ ] Получить draft
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

### Flow D — Profile setup

```text
Open Profile → Add skills → Add target roles → Save → Reload → Data persists
```

- [ ] Открыть Profile
- [ ] Заполнить имя
- [ ] Добавить target roles
- [ ] Добавить skills
- [ ] Добавить seniority
- [ ] Сохранить
- [ ] Перезагрузить страницу
- [ ] Проверить, что данные сохранились

### Flow E — Preferences setup

```text
Open Preferences → Add preferred roles / remote / skills → Save → Reload → Data persists
```

- [ ] Открыть Preferences
- [ ] Добавить preferred roles
- [ ] Добавить remote preference
- [ ] Добавить must-have skills
- [ ] Добавить nice-to-have skills
- [ ] Добавить excluded keywords
- [ ] Сохранить
- [ ] Перезагрузить страницу
- [ ] Проверить, что данные сохранились

### ✅ DoD

- [ ] Все ключевые пользовательские flows работают
- [ ] Backend tests проходят
- [ ] Frontend tests проходят
- [ ] Manual flow не сломан
- [ ] AI flow не сломан
- [ ] Profile flow работает
- [ ] Preferences flow работает
- [ ] Данные сохраняются корректно
- [ ] Ошибки отображаются пользователю

---

# 🔄 Рекомендуемый порядок реализации

## Step 1 — Закрыть Sprint 3 хвосты

```text
Epic 1 → Epic 2 → Epic 3 → Epic 4 → Epic 5
```

Цель этапа:

```text
RawJob → AI Draft → Reviewed Job
```

Пока это не закрыто, не начинать Profile / Preferences.

---

## Step 2 — Зафиксировать качество данных

```text
Epic 6
```

Цель этапа:

```text
Structured Job → Normalized Structured Job
```

---

## Step 3 — Добавить профиль пользователя

```text
Epic 7
```

Цель этапа:

```text
UserProfile exists and can be edited
```

---

## Step 4 — Добавить preferences

```text
Epic 8
```

Цель этапа:

```text
System knows what user wants
```

---

## Step 5 — Подготовить matching contract

```text
Epic 9
```

Цель этапа:

```text
Sprint 5 can start with scoring, not with model redesign
```

---

## Step 6 — Regression / E2E

```text
Epic 10
```

Цель этапа:

```text
Sprint 4 is actually usable
```

---

# 🎯 Sprint 4 Definition of Done

Спринт завершён, если:

- [ ] AI Draft flow из Sprint 3 полностью работает
- [ ] Draft можно создать, открыть, отредактировать, сохранить и сохранить как Job
- [ ] Job отображается в Jobs List
- [ ] RawJob остаётся неизменным
- [ ] `RawJob.processing_status` обновляется корректно
- [ ] `JobDraft.extraction_status` обновляется корректно
- [ ] `skills_source` работает как `manual / ai / mixed`
- [ ] Старый manual flow из Sprint 2 не сломан
- [ ] Normalization v1 работает для ключевых полей
- [ ] UserProfile можно создать и редактировать
- [ ] UserPreferences можно создать и редактировать
- [ ] Есть контракт `MatchResult` для Sprint 5
- [ ] Backend tests проходят
- [ ] Frontend tests проходят
- [ ] E2E flows проверены
- [ ] Matching score ещё не реализован
- [ ] Recommendation logic ещё не реализована
- [ ] RAG / embeddings / agents не добавлены

---

# 📦 Deliverable

В конце Sprint 4 должно быть:

- стабильный RawJob → AI Draft → Job flow
- исправленный lifecycle статусов
- завершённый Draft Editor
- frontend draft API client
- корректный `skills_source`
- normalization v1
- UserProfile model + API + UI
- UserPreferences model + API + UI
- MatchResult contract
- regression tests
- E2E checklist

---

# 🚫 What NOT to do in Sprint 4

- [ ] Не делать полноценный matching score
- [ ] Не делать recommendation APPLY / MAYBE / SKIP
- [ ] Не делать CV file upload parser
- [ ] Не делать embeddings
- [ ] Не делать pgvector
- [ ] Не делать RAG
- [ ] Не делать semantic search
- [ ] Не делать LangGraph
- [ ] Не делать multi-agent orchestration
- [ ] Не делать email ingestion
- [ ] Не делать cover letters
- [ ] Не делать auto-apply
- [ ] Не делать сложную taxonomy skills
- [ ] Не делать skill weights
- [ ] Не делать market analytics
- [ ] Не делать personal analytics
- [ ] Не делать agents

---

# 🚀 Next Sprint Preview — Sprint 5

Sprint 5 должен быть посвящён уже настоящему Matching MVP:

```text
Structured Job + UserProfile + Preferences
→ MatchResult
→ Fit Score
→ Skill gaps
→ Recommendation: APPLY / MAYBE / SKIP
```

В Sprint 5 можно будет делать:

- scoring service
- skill overlap
- missing skills
- seniority match
- remote/location preference match
- recommendation explanation
- match result UI
- сохранение match history, если потребуется

Но это будет возможно только если Sprint 4 реально закроет:

- данные
- профиль
- preferences
- стабильность AI Draft flow

---

# 🧭 Короткая формула Sprint 4

```text
Sprint 4 = закрыть AI Draft flow + привести данные в порядок + создать профиль пользователя + подготовить matching
```

Не “начать всё сразу”, а довести систему до точки, где следующий спринт сможет честно заниматься matching.

