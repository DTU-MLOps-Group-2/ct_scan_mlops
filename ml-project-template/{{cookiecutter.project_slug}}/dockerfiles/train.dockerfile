FROM ghcr.io/astral-sh/uv:python{{ cookiecutter.python_version }}-bookworm-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ src/
COPY configs/ configs/

# Default command
CMD ["uv", "run", "python", "-m", "{{ cookiecutter.project_slug }}.train"]
