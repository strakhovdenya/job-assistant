run-docker:
	docker compose up --build

start-docker:
	docker compose start

stop-docker:
	docker compose down

.PHONY: test test-backend test-frontend test-db-up

test: test-db-up test-backend test-frontend

test-db-up:
	docker compose up -d postgres

test-backend:
	uv run --project apps/backend --no-sync pytest tests/backend

test-frontend:
	@echo "Frontend tests are not configured yet"