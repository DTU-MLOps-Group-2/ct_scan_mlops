"""Utility and maintenance tasks."""

import os

from invoke import Context, task

WINDOWS = os.name == "nt"


@task
def clean_pyc(ctx: Context) -> None:
    """Remove Python bytecode files.

    Examples:
        invoke utils.clean-pyc
    """
    print("Removing Python bytecode files...")
    ctx.run("find . -type f -name '*.py[co]' -delete", warn=True, echo=True, pty=not WINDOWS)
    ctx.run("find . -type d -name '__pycache__' -delete", warn=True, echo=True, pty=not WINDOWS)
    print("Python bytecode cleaned")


@task
def clean_build(ctx: Context) -> None:
    """Remove build artifacts.

    Examples:
        invoke utils.clean-build
    """
    print("Removing build artifacts...")
    ctx.run("rm -rf build/ dist/ *.egg-info .eggs/", warn=True, echo=True, pty=not WINDOWS)
    print("Build artifacts cleaned")


@task
def clean_test(ctx: Context) -> None:
    """Remove test and coverage artifacts.

    Examples:
        invoke utils.clean-test
    """
    print("Removing test artifacts...")
    ctx.run("rm -rf .pytest_cache/ .coverage htmlcov/ .tox/", warn=True, echo=True, pty=not WINDOWS)
    print("Test artifacts cleaned")


@task
def clean_outputs(ctx: Context) -> None:
    """Remove training outputs and logs.

    Examples:
        invoke utils.clean-outputs
    """
    print("Removing training outputs...")
    ctx.run("rm -rf outputs/logs/ wandb/", warn=True, echo=True, pty=not WINDOWS)
    print("Training outputs cleaned")


@task(pre=[clean_pyc, clean_build, clean_test])
def clean_all(ctx: Context) -> None:
    """Clean all build, test, and Python artifacts.

    Examples:
        invoke utils.clean-all
    """
    print("\nAll artifacts cleaned!")


@task
def env_info(ctx: Context) -> None:
    """Show environment information.

    Examples:
        invoke utils.env-info
    """
    print("Environment Information")
    print("=" * 60)

    print("\nPython:")
    ctx.run("uv run python --version", echo=True, pty=not WINDOWS)

    print("\nuv:")
    ctx.run("uv --version", echo=True, pty=not WINDOWS)

    print("\nGit:")
    ctx.run("git --version", echo=True, pty=not WINDOWS)

    print("\nDocker:")
    ctx.run("docker --version", warn=True, echo=True, pty=not WINDOWS)

    print("\nGPU:")
    result = ctx.run(
        "nvidia-smi --query-gpu=name,driver_version --format=csv,noheader",
        warn=True,
        hide=True,
        pty=not WINDOWS,
    )
    if result and result.ok:
        print(f"  {result.stdout.strip()}")
    else:
        print("  No NVIDIA GPU detected")

    print("\n" + "=" * 60)


@task
def check_gpu(ctx: Context) -> None:
    """Check GPU availability and CUDA support.

    Examples:
        invoke utils.check-gpu
    """
    print("Checking GPU availability...\n")

    print("1. NVIDIA GPU:")
    ctx.run("nvidia-smi", warn=True, echo=True, pty=not WINDOWS)

    print("\n2. PyTorch CUDA:")
    ctx.run(
        'uv run python -c \'import torch; print(f"CUDA Available: {torch.cuda.is_available()}"); '
        'print(f"Device Count: {torch.cuda.device_count()}")\'',
        echo=True,
        pty=not WINDOWS,
    )


@task
def count_loc(ctx: Context) -> None:
    """Count lines of code in the project.

    Examples:
        invoke utils.count-loc
    """
    print("Lines of Code")
    print("=" * 60)
    ctx.run("find src/ -name '*.py' | xargs wc -l | sort -n", echo=True, pty=not WINDOWS)


@task
def find_todos(ctx: Context) -> None:
    """Find TODO/FIXME/HACK comments in code.

    Examples:
        invoke utils.find-todos
    """
    print("TODO/FIXME/HACK comments")
    print("=" * 60)
    ctx.run(
        "grep -rn 'TODO\\|FIXME\\|HACK\\|XXX' src/ tests/ --color=auto || echo 'No TODOs found!'",
        warn=True,
        echo=True,
        pty=not WINDOWS,
    )


@task
def port_check(ctx: Context, port: int = 8000) -> None:
    """Check if a port is in use.

    Args:
        port: Port number to check

    Examples:
        invoke utils.port-check
        invoke utils.port-check --port 8501
    """
    print(f"Checking port {port}...")
    result = ctx.run(f"lsof -i :{port}", warn=True, echo=True, pty=not WINDOWS)
    if not result or not result.ok:
        print(f"Port {port} is free")
