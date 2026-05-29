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
COPY static ./static
COPY scripts ./scripts
COPY data/processed ./data/processed

RUN uv run python scripts/build_index.py && uv run python scripts/build_embeddings.py

EXPOSE 8000

CMD ["sh", "-c", "uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
