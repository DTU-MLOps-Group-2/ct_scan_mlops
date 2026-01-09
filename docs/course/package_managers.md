# Package Managers Guide

Source: https://skaftenicki.github.io/dtu_mlops/s1_development_environment/package_manager/

## The Problem

Installing different package versions globally causes conflicts. When project A needs `torch==1.3.0` and project B needs `torch==2.0`, the last installation overwrites the previous one, breaking compatibility.

## The Solution

Use isolated virtual environments for each project, ensuring each maintains its own dependencies.

## Recommended Workflow

- Use `conda` to create virtual environments with specific Python versions
- Use `pip` to install packages within those environments
- This combination is safe with `conda>=4.6` due to built-in compatibility layers

## Key Commands

### Conda Operations

```bash
conda create --name my_environment python=3.11
conda env list
conda list
conda list --explicit > environment.yaml
conda env create --name <env-name> --file environment.yaml
conda activate <env-name>
conda deactivate
```

### Pip Operations

```bash
pip list
pip freeze > requirements.txt
pip install -r requirements.txt
pip install pipreqs
```

## Dependency Specification Format

Requirements files support seven operators:
- `package` (any version)
- `package == x.y.z` (exact)
- `package >= x.y.z` (at least)
- `package > x.y.z` (newer)
- `package <= x.y.z` (at most)
- `package < x.y.z` (older)
- `package ~= x.y.z` (compatible release)

## Best Practices

1. **Always specify versions** to ensure reproducibility
2. **Follow semantic versioning** (major.minor.patch)
3. **Use `pipreqs`** to generate minimal requirement files by scanning actual imports
4. **Export environments** as `environment.yaml` (conda) or `requirements.txt` (pip)
5. **Consider `mamba`** as a faster drop-in replacement for `conda`

## Alternative Package Managers

- **uv**: Fast Python package manager (76.1k GitHub stars)
- **Poetry**: Dependency management and packaging (34.1k stars)
- **Pipenv**: Combines pip and virtualenv (25.1k stars)

## UV Commands

```bash
uv venv                          # Create virtual environment
uv pip install -r requirements.txt
uv sync                          # Sync dependencies from pyproject.toml
uv lock                          # Generate lock file
```
