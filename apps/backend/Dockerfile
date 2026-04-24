FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /workspace

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Сначала копируем только файлы зависимостей для кэша
COPY pyproject.toml uv.lock ./
COPY apps/backend/pyproject.toml apps/backend/pyproject.toml
COPY apps/frontend/pyproject.toml apps/frontend/pyproject.toml

# Если packages/shared пока без pyproject.toml, эту строку не добавляй
# COPY packages/shared/pyproject.toml packages/shared/pyproject.toml

# Ставим зависимости backend-пакета
RUN uv sync --frozen --no-install-workspace --package backend

# Теперь копируем исходники
COPY apps/backend apps/backend
COPY packages/shared packages/shared

# Устанавливаем сам пакет после копирования кода
RUN uv sync --frozen --package backend

WORKDIR /workspace/apps/backend

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]