"""Data management tasks."""

import os
from pathlib import Path

from invoke import Context, task
from loguru import logger

WINDOWS = os.name == "nt"
PROJECT_NAME = "{{ cookiecutter.project_slug }}"


@task
def download(ctx: Context) -> None:
    """Download the dataset.

    Examples:
        invoke data.download
    """
    ctx.run(f"uv run python -m {PROJECT_NAME}.data download", echo=True, pty=not WINDOWS)


@task
def preprocess(ctx: Context) -> None:
    """Run data preprocessing pipeline.

    Examples:
        invoke data.preprocess
    """
    ctx.run(f"uv run python -m {PROJECT_NAME}.data preprocess", echo=True, pty=not WINDOWS)


@task
def stats(ctx: Context) -> None:
    """Show dataset statistics.

    Examples:
        invoke data.stats
    """
    data_dir = Path("data")
    if not data_dir.exists():
        logger.error("Data directory not found. Run 'invoke data.download' first.")
        return
    ctx.run(f"uv run python -m {PROJECT_NAME}.data stats", echo=True, pty=not WINDOWS)


@task
def validate(ctx: Context) -> None:
    """Validate data integrity.

    Examples:
        invoke data.validate
    """
    ctx.run(f"uv run python -m {PROJECT_NAME}.data validate", echo=True, pty=not WINDOWS)

{% if cookiecutter.use_dvc == "yes" %}

@task
def dvc_pull(ctx: Context) -> None:
    """Pull data from DVC remote.

    Examples:
        invoke data.dvc-pull
    """
    ctx.run("uv run dvc pull", echo=True, pty=not WINDOWS)


@task
def dvc_push(ctx: Context) -> None:
    """Push data to DVC remote.

    Examples:
        invoke data.dvc-push
    """
    ctx.run("uv run dvc push", echo=True, pty=not WINDOWS)
{% endif %}
