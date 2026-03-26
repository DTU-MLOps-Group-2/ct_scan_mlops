# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## IMPORTANT
- **ALWAYS activate environment first: `source .venv/bin/activate`**
- **After code changes run: `invoke quality.ruff`**
- **Always use `uv run` for Python commands** (e.g., `uv run python`, `uv run pytest`)
- **Always use `uv add` to install packages** (never `pip install`)

## Stack
- Python {{ cookiecutter.python_version }}, PyTorch Lightning
{%- if cookiecutter.use_hydra == "yes" %}, Hydra configs{% endif %}
- uv for package management, invoke for tasks
{%- if cookiecutter.use_wandb == "yes" %}
- W&B for experiment tracking
{%- endif %}
{%- if cookiecutter.use_dvc == "yes" %}
- DVC for data versioning
{%- endif %}

## Task Namespaces
Use `invoke <namespace>.<task>` or `invoke --list` to see all tasks.

**Namespaces:**
- `core` - Environment setup (bootstrap, sync, setup-dev)
- `data` - Data management (download, preprocess, stats, validate)
- `train` - Training (train, evaluate{% if cookiecutter.use_wandb == "yes" %}, sweep{% endif %})
- `quality` - Code quality (ruff, test, ci, security-check)
{%- if cookiecutter.use_docker == "yes" %}
- `docker` - Docker operations (build, run, clean)
{%- endif %}
- `utils` - Utilities (clean-all, env-info, check-gpu)

## Essential Commands
```bash
# Setup
invoke core.setup-dev           # Complete dev environment setup

# Development
invoke quality.ruff             # Lint + format
invoke quality.test             # Run tests
invoke quality.ci               # Full CI pipeline locally

# Data & Training
invoke data.download            # Download dataset
invoke train.train              # Train model
invoke train.evaluate --checkpoint path/to/model.ckpt
```

## Key Paths
- `src/{{ cookiecutter.project_slug }}/` - Main source code
- `configs/` - {% if cookiecutter.use_hydra == "yes" %}Hydra{% else %}YAML{% endif %} configs (model/, data/, train/)
- `tests/` - Unit tests
- `tasks/` - Invoke task modules
