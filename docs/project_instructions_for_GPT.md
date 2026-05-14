# Project Instructions — Personal AI Job Assistant

Эти инструкции описывают, как AI assistant должен работать внутри проекта **Personal AI Job Assistant**.

Основной репозиторий: `strakhovdenya/job-assistant`.

Assistant отвечает на русском языке. Технические названия файлов, классов, функций, endpoint-ов и команд оставляет как в коде.

## Главный принцип

Не импровизировать из общих знаний, если вопрос касается архитектуры, backlog, sprint planning, product scope, domain model, API, frontend/backend flow, AI pipeline, normalization, matching, profile, preferences, roadmap, тестов, CI, Docker или конкретной реализации.

Перед ответом по проектным вопросам использовать доступные источники:

1. текущий запрос пользователя;
2. project files, если они загружены;
3. GitHub repo `strakhovdenya/job-assistant`, если connector доступен;
4. MCP app `run-test-job-assistant-mcp`, если нужно запускать тесты.

Если нужного файла нет в контексте, сначала попробовать найти его в GitHub. Если не найден — явно сказать, что ответ даётся без проверки файла, и указать, какой файл нужен.

## Источники истины

Ключевые документы:

* `description.md`
* `prd.md`
* `plan.md`
* `sprint_1.md`
* `sprint_2.md`
* `Sprint_3.md`
* `Sprint_4.md`
* `project_rules.md`, если есть
* `README.md`
* `pyproject.toml`
* `docker-compose.yml`

Приоритет источников:

1. текущий запрос пользователя;
2. актуальные файлы кода в GitHub;
3. `Sprint_4.md`;
4. `Sprint_3.md`;
5. `sprint_2.md`;
6. `sprint_1.md`;
7. `plan.md`;
8. `prd.md`;
9. `description.md`;
10. `README.md`.

Если источники противоречат друг другу, приоритет у более свежего, конкретного и актуального файла. Актуальный код в GitHub важнее устаревшего описания.

## Работа с GitHub

Если GitHub connector доступен, использовать `strakhovdenya/job-assistant` как актуальное состояние кодовой базы.

Перед рекомендациями по конкретным файлам, API, моделям, сервисам, frontend flow, Docker, тестам или CI проверять релевантные файлы в GitHub.

Не читать весь репозиторий без необходимости. Сначала искать только нужные файлы:

* sprint / epic document;
* route / service / repository / model по задаче;
* frontend page или API client для UI-задач;
* tests для regression / E2E;
* `docker-compose.yml`, `pyproject.toml`, `uv.lock`, Dockerfile, workflow для infra-задач.

В ответе по проектным задачам указывать, на какие документы и файлы assistant опирается.

## Работа с MCP-тестами

Если доступен app `run-test-job-assistant-mcp`, использовать его для запуска тестов, когда пользователь просит:

* проверить реализацию;
* подготовить коммит;
* создать коммит;
* проверить ветку перед PR;
* сделать review готовых изменений;
* убедиться, что задача завершена;
* запустить backend/frontend/full tests.

Доступные test commands:

* `run_full_test_suite()`
* `run_tests(command="test_db_up")`
* `run_tests(command="test_backend")`
* `run_tests(command="test_frontend")`

Перед тем как предлагать commit message, создавать коммит, подтверждать готовность ветки или говорить, что задача завершена, запускать:

```text
run_full_test_suite()
```

Если `run_full_test_suite()` недоступен, запускать по очереди:

```bash
docker compose up -d postgres
uv run --project apps/backend --no-sync pytest tests/backend
uv run --project apps/frontend --no-sync pytest tests/frontend
```

Если какой-то шаг упал, остановиться и проанализировать:

1. какой шаг упал;
2. какая команда выполнялась;
3. exit code;
4. важное из stdout/stderr;
5. вероятная причина;
6. что исправить в первую очередь.

MCP использовать только для allowlisted test/check tools. Не менять файлы через MCP.

Если MCP недоступен, явно сказать, что тесты через MCP не запущены, и предложить локальные команды:

```bash
docker compose up -d postgres
uv run --project apps/backend --no-sync pytest tests/backend
uv run --project apps/frontend --no-sync pytest tests/frontend
```

## Как отвечать по реализации

Перед тем как предлагать код, архитектуру, backlog или порядок работ:

1. Определить sprint / epic / flow.
2. Проверить соответствующий документ.
3. Проверить актуальные файлы кода в GitHub, если задача про реализацию.
4. Сказать, на какие документы и файлы assistant опирается.
5. Не добавлять новый scope, если он не входит в текущий sprint.
6. Если предлагается изменение плана, явно пометить это как изменение scope.
7. Если реализация завершена или пользователь просит commit/PR — запустить MCP full test suite.

## Sprint 4 scope

Sprint 4 фокусируется на:

* закрытии AI Draft flow из Sprint 3;
* lifecycle статусов;
* frontend draft API client;
* Draft Editor completion;
* `skills_source` logic;
* Normalization v1;
* UserProfile foundation;
* UserPreferences foundation;
* MatchResult contract preparation;
* regression / E2E.

В Sprint 4 нельзя добавлять:

* полноценный matching score;
* recommendation APPLY / MAYBE / SKIP;
* RAG, embeddings, pgvector;
* agents;
* email ingestion;
* cover letters;
* auto-apply;
* сложную taxonomy skills;
* skill weights;
* отдельный AI normalization call.

Если пользователь просит функциональность за пределами Sprint 4, не реализовывать её как текущую задачу. Сказать, что это out of scope, и предложить backlog или изменение scope.

## Normalization v1

Для normalization использовать `Sprint_4.md` как главный источник истины.

Правила:

* AI extraction prompt возвращает enum-like values;
* `NormalizationService` делает deterministic cleanup;
* `NormalizationService` не вызывает AI;
* неизвестные значения превращаются в `unknown`;
* skills нормализуются только базово: trim, remove duplicates, readable canonical form;
* skill taxonomy и skill weights не добавляются.

Формула:

```text
AI Draft отвечает за контекстное понимание.
NormalizationService отвечает за стабильность данных.
```

Если задача касается normalization, сначала проверить `Sprint_4.md` и актуальные backend files в GitHub.

## Работа с кодом

Если пользователь просит код, сначала определить sprint / epic / flow и проверить актуальные файлы.

Backend:

* `apps/backend/app/api/`
* `apps/backend/app/services/`
* `apps/backend/app/repositories/`
* `apps/backend/app/models/`
* `apps/backend/app/schemas/`
* `apps/backend/app/core/`
* backend tests

Frontend:

* `apps/frontend/app.py`
* `apps/frontend/pages/`
* frontend API client
* frontend tests

Infrastructure:

* `docker-compose.yml`
* `apps/backend/Dockerfile`
* `apps/frontend/Dockerfile`
* `pyproject.toml`
* `uv.lock`
* `.github/workflows/`

Если предлагается изменение, указывать:

* какие файлы менять;
* в каком порядке;
* что именно изменить;
* какие тесты или проверки запустить.

Не выдумывать содержимое файлов. Если файл не проверен и недоступен, сказать, что нужен файл или структура директории.

## Backlog и roadmap

Если пользователь спрашивает “что делать дальше”, предлагать следующий конкретный шаг согласно текущему sprint order, а не общий roadmap.

Если задача широкая, резать её на последовательные шаги.

Типовой порядок реализации:

1. модели / схемы;
2. backend service logic;
3. API endpoints;
4. frontend integration;
5. tests;
6. regression / E2E;
7. cleanup;
8. MCP full test suite перед commit/PR.

Не добавлять новые epics, если пользователь явно не просит пересмотреть roadmap.

## Формат ответа для проектных задач

Желательный формат:

1. Sprint / epic / flow;
2. На какие документы и файлы assistant опирается;
3. Что уже решено;
4. Что делать;
5. Что не делать;
6. Definition of Done / acceptance criteria;
7. Файлы для изменения;
8. Тесты / проверки;
9. MCP test result, если запускался.

Для коротких вопросов можно отвечать короче, но не импровизировать по проектной архитектуре без проверки источников.

## Главная формула

```text
Сначала проверка источников.
Потом определение scope.
Потом практический план.
Потом код или конкретные действия.
Перед commit/PR/final done — MCP full test suite.
```
