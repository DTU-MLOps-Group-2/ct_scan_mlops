# Good Coding Practice Guide

Source: https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/good_coding_practice/

## Core Philosophy

**Foundational Principle**: "Code is read more often than it is written" (Guido Van Rossum)

This emphasizes prioritizing readability and consistency above all else.

## Documentation Standards

**Key Principle**: "Code tells you how; Comments tell you why" (Jeff Atwood)

### Best Practices
- Avoid under-documentation (missing explanations of complex logic)
- Avoid over-documentation (excessive detail that discourages reading)
- Add docstrings to functions/methods using standardized keywords
- In deep learning, annotate tensor shape transformations with comments

### Docstring Format

```python
def function(param1: int, param2: str) -> bool:
    """Brief description of what the function does.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of return value

    Example:
        >>> function(1, "test")
        True
    """
    pass
```

## Code Styling (PEP8 Compliance)

### Recommended Tools
- **ruff**: Fast linter/formatter (recommended over legacy `flake8`)

### Configuration in `pyproject.toml`

```toml
[tool.ruff]
lint.select = ["I"]  # Organize imports
line-length = 120    # More practical than PEP8's 79 characters

[tool.ruff.lint.isort]
known-first-party = ["your_package"]
```

### Import Organization

Organize imports in three blocks:
1. Built-in Python packages (`os`, `sys`)
2. Third-party dependencies (`torch`, `numpy`)
3. Local package imports

### Commands

```bash
ruff check .      # Identify style violations
ruff format .     # Apply automatic corrections
ruff check --fix  # Auto-fix violations
```

## Type Hints

### Benefits
- Clarifies expected input/output types
- Enables IDE autocompletion and error detection
- Works with static type checker `mypy`

### Syntax Examples

```python
# Python 3.10+
def process(data: int | float | list[int]) -> dict[str, any]:
    pass

# Earlier versions
from typing import Union, List, Dict, Any
def process(data: Union[int, float, List[int]]) -> Dict[str, Any]:
    pass

# Optional parameters
from typing import Optional
def fetch(url: str, timeout: Optional[int] = None) -> str:
    pass
```

### Type Checking

```bash
pip install mypy
mypy filename.py
```

## Implementation Checklist

1. Install and configure linting/formatting tools: `pip install ruff mypy`
2. Run `ruff check .` to identify style violations
3. Apply `ruff format .` for automatic corrections
4. Add type hints systematically to function signatures
5. Write docstrings with clear parameter descriptions
6. Use `mypy` to validate type correctness

## Critical Takeaway

Consistency matters more than perfect adherence to any single standard. Establish conventions and maintain them throughout your project.
