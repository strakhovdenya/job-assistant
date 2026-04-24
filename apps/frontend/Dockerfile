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

# Если shared ещё не оформлен как пакет, не копируй его pyproject отдельно
# COPY packages/shared/pyproject.toml packages/shared/pyproject.toml

# Ставим зависимости frontend-пакета
RUN uv sync --frozen --no-install-workspace --package frontend

# Теперь копируем исходники
COPY apps/frontend apps/frontend
COPY packages/shared packages/shared

# Устанавливаем сам frontend после копирования кода
RUN uv sync --frozen --package frontend

WORKDIR /workspace/apps/frontend

CMD ["uv", "run", "--package", "frontend", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]