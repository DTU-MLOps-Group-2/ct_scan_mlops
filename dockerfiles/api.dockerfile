# API dockerfile for serving predictions
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS base

WORKDIR /app

COPY uv.lock uv.lock
COPY pyproject.toml pyproject.toml

RUN uv sync --frozen --no-install-project

COPY src/ src/
COPY models/ models/

RUN uv sync --frozen

EXPOSE 8000

ENTRYPOINT ["uv", "run", "uvicorn", "ct_scan_mlops.api:app", "--host", "0.0.0.0", "--port", "8000"]
CMD []
