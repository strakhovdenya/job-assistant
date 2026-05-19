# MCP Test Server

This repository can be tested through a dedicated MCP server:

`strakhovdenya/run-test-job-assistant-mcp`

## Purpose

The MCP server exposes a small allowlisted set of commands for running Job Assistant checks from an AI assistant.

It is intended for:

- running backend tests
- running frontend tests
- starting required test dependencies
- running the full test suite safely
- opening a ChatGPT App widget with a button, progress bar and logs

## Available commands

- `open_test_runner_widget` — opens the ChatGPT App widget for running the full suite with visible progress and logs. Prefer this when the user asks to run the full test suite with a UI/progress panel.
- `test_db_up` — starts PostgreSQL via Docker Compose.
- `test_backend` — runs backend pytest suite.
- `test_frontend` — runs frontend pytest suite.
- `run_full_test_suite` — runs DB setup, backend tests and frontend tests synchronously. Use this only when widget progress is not needed.
- `start_full_test_suite` — starts the full suite in the background and returns a `run_id`. This is intended for the widget, not normal chat.
- `get_test_suite_status` — returns status, progress and logs for a background run. This is intended for widget polling.

## Recommended assistant behavior

Use the narrowest safe MCP command for the user's request:

- If the user asks to run the full suite with visible progress/logs, call `open_test_runner_widget`.
- If the user asks to run backend tests only, call `run_tests(command="test_backend")`.
- If the user asks to run frontend tests only, call `run_tests(command="test_frontend")`.
- If PostgreSQL must be started, call `run_tests(command="test_db_up")`.
- Do not use arbitrary shell commands for test execution.

## ChatGPT App widget flow

The widget flow is polling-based because ChatGPT does not stream arbitrary long-running tool output directly into a message while the tool is still running.

Expected flow:

1. Assistant calls `open_test_runner_widget`.
2. The widget renders a `Run Full Test Suite` button.
3. The widget calls `start_full_test_suite` and receives a `run_id`.
4. The widget polls `get_test_suite_status(run_id)` every second.
5. The widget renders status, progress bar and logs.
6. Polling stops when status is `passed` or `failed`.

## Suggested ChatGPT Project Settings

Paste the following into the ChatGPT project instructions. It is intentionally short and below the 8000 character limit.

```text
This project is for `strakhovdenya/job-assistant`.

Use the MCP server `strakhovdenya/run-test-job-assistant-mcp` for Job Assistant checks.

When the user asks to run the full Job Assistant test suite with visible progress, logs, a panel, UI, or widget, call `open_test_runner_widget`.

The widget handles the long-running flow itself: it calls `start_full_test_suite`, then polls `get_test_suite_status(run_id)` until the run is `passed` or `failed`.

Do not call `start_full_test_suite` directly in normal chat unless a widget or polling flow is already active.

For targeted checks, use the allowlisted MCP test tool:
- backend only: `run_tests(command="test_backend")`
- frontend only: `run_tests(command="test_frontend")`
- PostgreSQL dependency: `run_tests(command="test_db_up")`

Use `run_full_test_suite` only when the user explicitly wants a synchronous full-suite result without widget progress.

Do not use arbitrary shell commands for tests. Prefer the allowlisted MCP tools.

If tests fail, summarize the failed step, exit code, relevant stdout/stderr, and suggest the next code or test fix.
```

## Related repository

See: `strakhovdenya/run-test-job-assistant-mcp`
