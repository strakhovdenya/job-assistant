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

## Available commands

- `test_db_up` — starts PostgreSQL via Docker Compose
- `test_backend` — runs backend pytest suite
- `test_frontend` — runs frontend pytest suite
- `run_full_test_suite` — runs DB setup, backend tests, frontend tests

## Related repository

See: `strakhovdenya/run-test-job-assistant-mcp`