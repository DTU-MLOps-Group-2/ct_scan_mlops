# ML Project Code Structure Guide

Source: https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/code_structure/

## Core Organization Principles

**Standardized Structure Benefits**: Using templates like cookiecutter provides consistency across teams, enabling developers to understand each other's code faster and making projects easier to maintain.

**Key Insight**: "A Big Ball of Mud is a haphazardly structured, sprawling, sloppy...jungle" demonstrating why intentional organization matters from project inception.

## Essential File Structure

### Python Package Basics
- `__init__.py` marks directories as Python packages
- `pyproject.toml` provides standardized project metadata (modern approach)
- `setup.py + setup.cfg` (legacy, still encountered)

### Directory Layout (src-layout recommended)

```
project_root/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── data.py
│       ├── model.py
│       ├── train.py
│       ├── evaluate.py
│       └── visualize.py
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── reports/
│   └── figures/
├── tests/
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Critical Files for ML Projects

### pyproject.toml

Should include:
- `[build-system]` section (setuptools, wheel)
- `[project]` metadata (name, version, dependencies)
- Tool configurations (ruff, pytest, etc.)

### requirements.txt

Lists all package dependencies with versions.

### tasks.py

Uses invoke framework for defining common project tasks.

## Development Workflow

Install projects in editable mode:
```bash
pip install -e .
```

This enables iterative development without reinstalling after code changes.

## Project-Specific Modules

| Module | Purpose |
|--------|---------|
| `data.py` | Raw data processing, normalization, saving processed datasets |
| `model.py` | Neural network architecture definition |
| `train.py` | Training loop, model checkpointing, statistics logging |
| `evaluate.py` | Model loading, performance metrics on test sets |
| `visualize.py` | Feature extraction, dimensionality reduction (t-SNE), visualization |

## Best Practices Summary

1. Always run scripts from project root for consistent relative paths
2. Use templates as guides—customize for project needs
3. Maintain organized folder hierarchies separating raw/processed data
4. Document processes in README files
5. Save trained models and visualizations systematically
6. Keep tests in a separate `tests/` directory
7. Store configuration in dedicated config files, not hardcoded in scripts
