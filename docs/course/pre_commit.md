# Pre-commit Guide

Source: https://skaftenicki.github.io/dtu_mlops/s5_continuous_integration/pre_commit/

## Core Purpose

Pre-commit automates code quality checks by inserting tasks between `git commit` and `git push`, ensuring consistent standards without manual intervention.

## Installation & Setup

```bash
pip install pre-commit
pre-commit sample-config > .pre-commit-config.yaml
pre-commit install
```

## Configuration File

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: ["--fix"]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

## Common Hooks

| Hook | Purpose |
|------|---------|
| `trailing-whitespace` | Removes trailing spaces |
| `end-of-file-fixer` | Ensures proper file endings |
| `check-yaml` | Validates YAML syntax |
| `check-added-large-files` | Prevents large file commits |
| `check-json` | Validates JSON structure |
| `check-merge-conflict` | Checks for conflict markers |
| `detect-private-key` | Prevents committing private keys |

## Commands

```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files

# Update hook versions
pre-commit autoupdate

# Skip hooks (emergency only)
git commit -m "message" --no-verify
```

## Disabling Pre-commit

```bash
# Temporarily
git commit --no-verify

# Permanently
rm .git/hooks/pre-commit
# or
pre-commit uninstall
```

## GitHub Actions Integration

```yaml
name: Pre-commit

on: [push, pull_request]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - uses: pre-commit/action@v3.0.1

      - uses: stefanzweifel/git-auto-commit-action@v5
        if: failure()
        with:
          commit_message: "style: auto-fix pre-commit issues"
```

## Scheduled Updates

```yaml
name: Pre-commit Autoupdate

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  autoupdate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install pre-commit
      - run: pre-commit autoupdate
      - uses: peter-evans/create-pull-request@v5
        with:
          title: "Update pre-commit hooks"
          branch: pre-commit-autoupdate
```

## Best Practices

1. Install pre-commit hooks immediately after cloning
2. Run `pre-commit run --all-files` before first commit
3. Keep hooks updated with `pre-commit autoupdate`
4. Use `--no-verify` sparingly and only in emergencies
5. Include pre-commit checks in CI/CD pipeline
6. Configure hooks to auto-fix where possible
