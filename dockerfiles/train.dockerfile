# CPU-only training dockerfile (lightweight, for CI/testing)
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS base

WORKDIR /app

COPY uv.lock uv.lock
COPY pyproject.toml pyproject.toml

RUN uv sync --frozen --no-install-project

COPY src/ src/
COPY configs/ configs/

RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "python", "-m", "ct_scan_mlops.train"]
CMD []
