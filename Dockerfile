FROM python:3.10-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml .
RUN uv venv .venv && \
    uv sync


FROM python:3.10-slim

COPY --from=builder /app/.venv /app/.venv

WORKDIR /app

COPY main.py .
COPY mail_template.html .

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "main.py"]