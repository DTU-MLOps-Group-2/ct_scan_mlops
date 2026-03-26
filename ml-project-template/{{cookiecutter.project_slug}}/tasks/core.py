"""Core environment setup and maintenance tasks."""

import os

from invoke import Context, task

WINDOWS = os.name == "nt"
PROJECT_NAME = "{{ cookiecutter.project_slug }}"


@task
def bootstrap(ctx: Context, name: str = ".venv") -> None:
    """Create virtual environment and install dependencies.

    Examples:
        invoke core.bootstrap
    """
    ctx.run(f"uv venv {name}", echo=True, pty=not WINDOWS)
    ctx.run("uv sync", echo=True, pty=not WINDOWS)
    print(f"\n  Environment created at {name}")
    print(f"To activate: source {name}/bin/activate")


@task
def sync(ctx: Context) -> None:
    """Install/sync all dependencies.

    Examples:
        invoke core.sync
    """
    ctx.run("uv sync", echo=True, pty=not WINDOWS)


@task
def setup_dev(ctx: Context) -> None:
    """Complete development environment setup (one command).

    Examples:
        invoke core.setup-dev
    """
    print("Setting up development environment...\n")

    print("1. Installing dependencies...")
    ctx.run("uv sync --dev", echo=True, pty=not WINDOWS)

    print("\n2. Installing pre-commit hooks...")
    ctx.run("uv run pre-commit install", echo=True, pty=not WINDOWS)

    print("\n3. Checking environment...")
    ctx.run("uv run python --version", echo=True, pty=not WINDOWS)
    ctx.run(
        'uv run python -c \'import torch; print(f"PyTorch: {torch.__version__}")\'',
        echo=True,
        pty=not WINDOWS,
    )

    print("\n4. Checking GPU availability...")
    result = ctx.run("nvidia-smi", warn=True, hide=True, pty=not WINDOWS)
    if result and result.ok:
        ctx.run(
            'uv run python -c \'import torch; print(f"CUDA available: {torch.cuda.is_available()}")\'',
            echo=True,
            pty=not WINDOWS,
        )
    else:
        print("   No NVIDIA GPU detected (CPU-only mode)")

    print("\nDevelopment environment ready!")
    print("Next steps:")
    print("  - Run 'source .venv/bin/activate' to activate")
    print("  - Run 'invoke data.download' to get data")
    print("  - Run 'invoke train.train' to start training")


@task
def python(ctx: Context) -> None:
    """Check Python path and version.

    Examples:
        invoke core.python
    """
    ctx.run("which python" if os.name != "nt" else "where python", echo=True, pty=not WINDOWS)
    ctx.run("python --version", echo=True, pty=not WINDOWS)
