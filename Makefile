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
	@powershell -NoProfile -Command "\
		Write-Host 'Waiting for Postgres...'; \
		for ($$i = 1; $$i -le 10; $$i++) { \
			docker compose exec -T postgres pg_isready -U job_assistant -d job_assistant; \
			if ($$LASTEXITCODE -eq 0) { \
				Write-Host 'Postgres is ready'; \
				exit 0; \
			}; \
			Start-Sleep -Seconds 1; \
		}; \
		Write-Error 'Postgres did not become ready in time'; \
		exit 1"

test-backend:
	uv run --project apps/backend --no-sync pytest tests/backend

test-frontend:
	uv run --project apps/frontend --no-sync pytest tests/frontend