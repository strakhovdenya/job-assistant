# Project Rules — Personal AI Job Assistant

## 1. Source-first rule

Любая архитектурная, продуктовая или sprint-related задача должна начинаться с проверки project files.

Не принимать решения “из головы”, если есть соответствующий документ.

## 2. Sprint scope rule

Всегда соблюдать scope текущего sprint.

Если задача относится к будущему sprint, не реализовывать её раньше времени без явного решения пользователя.

## 3. Current sprint

Текущий sprint: Sprint 4.

Главная цель Sprint 4:

- стабилизировать AI Draft flow
- закрыть хвосты Sprint 3
- подготовить данные к Matching MVP
- добавить UserProfile foundation
- добавить UserPreferences foundation
- подготовить MatchResult contract

## 4. Sprint 4 implementation order

Порядок выполнения Sprint 4:

1. Sprint 3 Stabilization
2. Processing Status Cleanup
3. Frontend Draft API Client
4. AI Draft Editor Completion
5. Skills Source Logic
6. Normalization v1
7. User Profile Foundation
8. Preferences Foundation
9. Matching Contract Preparation
10. Regression & E2E

Нельзя перескакивать к Profile / Preferences, пока AI Draft flow не стабилен.

## 5. AI Draft flow

Основной flow:

RawJob → AI Draft → User Review/Edit → Save as Job

AI не сохраняет Job напрямую.

Пользователь остаётся источником истины.

## 6. Normalization v1

Использовать гибридную стратегию:

AI Extraction Prompt → JobDraft with enum-like values → User Review/Edit → NormalizationService → Structured Job

AI понимает контекст.
NormalizationService гарантирует стабильность данных.

Запрещено:

- отдельный AI normalization call
- второй LLM pipeline после draft
- большая regex-система
- skill taxonomy
- skill weights

## 7. Matching

В Sprint 4 matching score не реализуется.

Разрешено только подготовить контракт MatchResult.

Полноценный Matching MVP — Sprint 5.

## 8. When unsure

Если информации не хватает:

- попросить нужный файл
- или явно сказать, какой документ нужен
- не придумывать недостающие решения