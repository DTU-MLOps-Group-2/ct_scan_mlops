# GitHub Actions Guide

Source: https://skaftenicki.github.io/dtu_mlops/s5_continuous_integration/github_actions/

## Core Workflow Structure

A GitHub Actions workflow file consists of five key components:

1. **Name**: Identifies the workflow
2. **Triggers**: Specifies events (push, pull_request, schedule)
3. **Jobs**: Parallel or dependent task groups
4. **Runners**: Operating systems where workflows execute
5. **Steps**: Individual commands and actions

## Basic Workflow Configuration

```yaml
name: Tests

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements_tests.txt

      - name: Run tests
        run: pytest tests/
```

## Matrix Testing Strategy

Run tests across multiple configurations:

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

## Code Quality Workflow

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install tools
        run: pip install ruff mypy

      - name: Check formatting
        run: ruff format --check .

      - name: Lint
        run: ruff check .

      - name: Type check
        run: mypy src/
```

## DVC Data Authentication

```yaml
- name: Setup GCP credentials
  env:
    GCP_CREDENTIALS: ${{ secrets.GCP_CREDENTIALS }}
  run: |
    echo "$GCP_CREDENTIALS" > credentials.json
    gcloud auth activate-service-account --key-file credentials.json

- name: Pull data
  run: dvc pull
```

## Docker Build and Push

```yaml
name: Docker

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to GCR
        uses: docker/login-action@v3
        with:
          registry: gcr.io
          username: _json_key
          password: ${{ secrets.GCP_CREDENTIALS }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: gcr.io/${{ secrets.GCP_PROJECT }}/app:${{ github.sha }}
```

## Dependabot Configuration

`.github/dependabot.yaml`:
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

## Branch Protection Rules

1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable "Require status checks to pass"
4. Select required workflows

## Secrets Management

1. Go to Settings → Secrets and variables → Actions
2. Add repository secrets (e.g., `GCP_CREDENTIALS`)
3. Access in workflows via `${{ secrets.SECRET_NAME }}`

## Best Practices

1. **Cache dependencies** to reduce workflow runtime
2. **Use specific action versions** (e.g., `@v4` not `@latest`)
3. **Separate workflow files** for testing, formatting, and deployment
4. **Set `fail-fast: false`** for matrix builds to see all failures
5. **Use branch protection** to enforce passing checks
6. **Store secrets securely** in GitHub Secrets, never in code
