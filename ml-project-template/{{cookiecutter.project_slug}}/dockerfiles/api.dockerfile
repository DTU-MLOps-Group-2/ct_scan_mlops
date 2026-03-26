FROM ghcr.io/astral-sh/uv:python{{ cookiecutter.python_version }}-bookworm-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ src/
COPY configs/ configs/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "{{ cookiecutter.project_slug }}.api:app", "--host", "0.0.0.0", "--port", "8000"]
