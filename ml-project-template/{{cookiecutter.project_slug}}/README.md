# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Quick Start

### Prerequisites
- Python {{ cookiecutter.python_version }}+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd {{ cookiecutter.project_slug }}

# One-command setup (creates venv, installs deps, pre-commit hooks)
invoke core.setup-dev

# Activate the environment
source .venv/bin/activate
```

### Development Workflow
```bash
# Lint and format code
invoke quality.ruff

# Run tests
invoke quality.test

# Run full CI pipeline locally
invoke quality.ci
```

### Training
```bash
# Download data
invoke data.download

# Train model
invoke train.train
{%- if cookiecutter.use_hydra == "yes" %}

# Train with custom config overrides
invoke train.train --args "model=default train.max_epochs=100 train.lr=0.001"
{%- endif %}

# Evaluate model
invoke train.evaluate --checkpoint outputs/checkpoints/best.ckpt
```
{%- if cookiecutter.use_wandb == "yes" %}

### Hyperparameter Sweeps
```bash
# Create a W&B sweep
invoke train.sweep

# Run a sweep agent
invoke train.sweep-agent --sweep-id ENTITY/PROJECT/SWEEP_ID
```
{%- endif %}
{%- if cookiecutter.use_docker == "yes" %}

### Docker
```bash
# Build images
invoke docker.build

# Train in container
invoke docker.train

# Run API in container
invoke docker.api
```
{%- endif %}

## Project Structure
```
{{ cookiecutter.project_slug }}/
├── src/{{ cookiecutter.project_slug }}/    # Source code
│   ├── model.py                            # Model definitions
│   ├── data.py                             # Data loading
│   ├── train.py                            # Training entrypoint
│   ├── evaluate.py                         # Evaluation
│   ├── api.py                              # FastAPI serving
│   └── utils.py                            # Utilities
├── configs/                                # Configuration files
│   ├── config.yaml                         # Main config
│   ├── model/                              # Model configs
│   ├── data/                               # Data configs
│   └── train/                              # Training configs
├── tasks/                                  # Invoke task modules
├── tests/                                  # Unit tests
├── dockerfiles/                            # Docker build files
├── notebooks/                              # Jupyter notebooks
├── data/                                   # Dataset directory
├── outputs/                                # Training outputs
├── models/                                 # Saved models
├── pyproject.toml                          # Project configuration
└── CLAUDE.md                               # AI assistant instructions
```

## All Tasks
Run `invoke --list` to see all available tasks, organized by namespace:
- **core** - Environment setup
- **data** - Data management
- **train** - Training and evaluation
- **quality** - Code quality and testing
{%- if cookiecutter.use_docker == "yes" %}
- **docker** - Container operations
{%- endif %}
- **utils** - Maintenance utilities

## License
{{ cookiecutter.license }}
