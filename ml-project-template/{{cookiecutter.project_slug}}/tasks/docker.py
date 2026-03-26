"""Docker container and image management tasks."""

import os
from pathlib import Path

from invoke import Context, task
from loguru import logger

WINDOWS = os.name == "nt"
PROJECT_NAME = "{{ cookiecutter.project_slug }}"


def check_docker_available(ctx: Context) -> bool:
    """Check if Docker is installed and running."""
    try:
        result = ctx.run("docker info", hide=True, warn=True, pty=not WINDOWS)
        return result.ok
    except Exception:
        return False


@task
def build(ctx: Context, progress: str = "plain") -> None:
    """Build docker images.

    Examples:
        invoke docker.build
    """
    if not check_docker_available(ctx):
        logger.error("Docker is not running. Please start Docker and try again.")
        return

    ctx.run(
        f"docker build -t {PROJECT_NAME}-train:latest . -f dockerfiles/train.dockerfile --progress={progress}",
        echo=True,
        pty=not WINDOWS,
    )
    ctx.run(
        f"docker build -t {PROJECT_NAME}-api:latest . -f dockerfiles/api.dockerfile --progress={progress}",
        echo=True,
        pty=not WINDOWS,
    )


@task
def train(ctx: Context, gpu: bool = False, args: str = "") -> None:
    """Run training in Docker container.

    Args:
        gpu: Enable GPU support
        args: Additional training arguments

    Examples:
        invoke docker.train
        invoke docker.train --gpu
    """
    if not check_docker_available(ctx):
        logger.error("Docker is not running. Please start Docker and try again.")
        return

    cwd = Path.cwd()
    gpu_flag = "--gpus all" if gpu else ""
    ctx.run(
        f"docker run --rm {gpu_flag} "
        f"-v {cwd}/data:/app/data "
        f"-v {cwd}/models:/app/models "
        f"-v {cwd}/outputs:/app/outputs "
        f"{PROJECT_NAME}-train:latest {args}",
        echo=True,
        pty=not WINDOWS,
    )


@task
def api(ctx: Context, port: int = 8000) -> None:
    """Run API in Docker container.

    Examples:
        invoke docker.api
        invoke docker.api --port 8080
    """
    if not check_docker_available(ctx):
        logger.error("Docker is not running. Please start Docker and try again.")
        return

    ctx.run(
        f"docker run -p {port}:8000 "
        f"-v $(pwd)/models:/app/models "
        f"{PROJECT_NAME}-api:latest",
        echo=True,
        pty=not WINDOWS,
    )


@task
def clean(ctx: Context, all: bool = False) -> None:
    """Clean up Docker images and containers.

    Args:
        all: Remove all unused images (not just dangling ones)

    Examples:
        invoke docker.clean
        invoke docker.clean --all
    """
    if not check_docker_available(ctx):
        logger.error("Docker is not running. Please start Docker and try again.")
        return

    print("Removing stopped containers...")
    ctx.run("docker container prune -f", echo=True, pty=not WINDOWS)

    if all:
        print("Removing all unused images...")
        ctx.run("docker image prune -a -f", echo=True, pty=not WINDOWS)
    else:
        print("Removing dangling images...")
        ctx.run("docker image prune -f", echo=True, pty=not WINDOWS)

    print("\nDocker cleanup complete!")
