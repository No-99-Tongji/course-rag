FROM node:22-slim AS frontend-builder

WORKDIR /frontend
COPY frontend/package*.json ./
RUN HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= http_proxy= https_proxy= all_proxy= npm install
COPY frontend ./
RUN HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= http_proxy= https_proxy= all_proxy= npm run build

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev

COPY app ./app
COPY scripts ./scripts
COPY data/processed ./data/processed
COPY --from=frontend-builder /static ./static

EXPOSE 8000

CMD ["sh", "-c", "uv run python scripts/build_index.py && uv run python scripts/build_embeddings.py && uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
