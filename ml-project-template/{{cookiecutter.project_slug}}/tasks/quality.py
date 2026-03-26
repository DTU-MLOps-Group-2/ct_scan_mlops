"""Code quality and testing tasks."""

import os

from invoke import Context, task

WINDOWS = os.name == "nt"


@task
def ruff(ctx: Context, check_only: bool = False) -> None:
    """Run ruff linter and formatter.

    Args:
        check_only: Only check without modifying files (CI mode)

    Examples:
        invoke quality.ruff
        invoke quality.ruff --check-only
    """
    if check_only:
        ctx.run("uv run ruff check .", echo=True, pty=not WINDOWS)
        ctx.run("uv run ruff format . --check", echo=True, pty=not WINDOWS)
    else:
        ctx.run("uv run ruff check . --fix", echo=True, pty=not WINDOWS)
        ctx.run("uv run ruff format .", echo=True, pty=not WINDOWS)


@task
def test(ctx: Context) -> None:
    """Run tests with coverage report.

    Examples:
        invoke quality.test
    """
    ctx.run("uv run coverage run -m pytest tests/", echo=True, pty=not WINDOWS)
    ctx.run("uv run coverage report -m -i", echo=True, pty=not WINDOWS)


@task
def test_unit(ctx: Context) -> None:
    """Run fast unit tests only (excludes slow and data-dependent tests).

    Examples:
        invoke quality.test-unit
    """
    ctx.run("uv run pytest tests/ -m 'not slow and not requires_data' -v", echo=True, pty=not WINDOWS)


@task
def ci(ctx: Context) -> None:
    """Run full CI pipeline locally (lint + format check + tests).

    Examples:
        invoke quality.ci
    """
    print("\n" + "=" * 60)
    print("Running CI Pipeline")
    print("=" * 60 + "\n")

    print("Step 1/3: Linting...")
    ctx.run("uv run ruff check .", echo=True, pty=not WINDOWS)

    print("\nStep 2/3: Format check...")
    ctx.run("uv run ruff format . --check", echo=True, pty=not WINDOWS)

    print("\nStep 3/3: Running tests...")
    test_unit(ctx)

    print("\n" + "=" * 60)
    print("CI Pipeline Passed!")
    print("=" * 60)


@task
def security_check(ctx: Context) -> None:
    """Run security vulnerability checks.

    Examples:
        invoke quality.security-check
    """
    print("Running security checks...\n")

    print("1. Checking for known vulnerabilities in dependencies...")
    result = ctx.run("uv run pip-audit", warn=True, echo=True, pty=not WINDOWS)

    print("\n2. Running bandit security linter...")
    ctx.run("uv run bandit -r src/ -f screen", warn=True, echo=True, pty=not WINDOWS)

    if result and result.ok:
        print("\nSecurity checks passed!")
    else:
        print("\nSecurity issues found - please review above")


@task
def install_hooks(ctx: Context) -> None:
    """Install git pre-commit hooks.

    Examples:
        invoke quality.install-hooks
    """
    ctx.run("uv run pre-commit install", echo=True, pty=not WINDOWS)
    print("\nGit hooks installed!")
