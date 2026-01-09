# Documentation Guide

Source: https://skaftenicki.github.io/dtu_mlops/s10_extra/documentation/

## MkDocs Setup

### Installation

```bash
pip install "mkdocs-material>=4.8.0"
pip install mkdocstrings[python]
```

### Configuration (`mkdocs.yaml`)

```yaml
site_name: My Project
site_author: Your Name
docs_dir: docs/

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - search.suggest

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true

nav:
  - Home: index.md
  - API Reference:
    - Model: api/model.md
    - Data: api/data.md
  - Tutorials:
    - Getting Started: tutorials/quickstart.md
```

## Local Development

```bash
# Preview with auto-reload
mkdocs serve

# Build static site
mkdocs build

# Faster rebuild (dirty mode)
mkdocs build --dirty
```

## API Documentation

### Auto-generate from Docstrings

In your markdown files:

```markdown
# Model API

::: src.model.MyModel
    options:
      show_source: true
      heading_level: 2

::: src.model.train
```

### Docstring Format

```python
def train(model: nn.Module, data: DataLoader, epochs: int = 10) -> dict:
    """Train a neural network model.

    Args:
        model: PyTorch model to train
        data: Training data loader
        epochs: Number of training epochs

    Returns:
        Dictionary containing training metrics:
        - loss: Final training loss
        - accuracy: Final training accuracy

    Example:
        >>> model = MyModel()
        >>> loader = DataLoader(dataset)
        >>> metrics = train(model, loader, epochs=5)
        >>> print(metrics['accuracy'])
        0.95
    """
```

## GitHub Pages Deployment

### Workflow (`.github/workflows/deploy_docs.yaml`)

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install mkdocs-material
          pip install mkdocstrings[python]

      - name: Deploy
        run: mkdocs gh-deploy --force
```

### GitHub Configuration

1. Go to Settings → Pages
2. Select "Deploy from a branch"
3. Choose `gh-pages` branch and `/(root)` folder

Site deploys to: `https://<username>.github.io/<repo-name>/`

## Documentation Structure

```
docs/
├── index.md          # Home page
├── installation.md   # Setup instructions
├── quickstart.md     # Getting started
├── api/
│   ├── model.md      # Model API reference
│   └── data.md       # Data API reference
├── tutorials/
│   └── example.md    # Step-by-step guides
└── assets/
    └── images/       # Documentation images
```

## Best Practices

1. **Write docstrings first**: Document as you code
2. **Include examples**: Show usage in docstrings
3. **Use type hints**: They appear in documentation
4. **Keep it updated**: Stale docs are worse than no docs
5. **Add images**: Visualize complex concepts
6. **Cross-reference**: Link related sections
7. **Test examples**: Ensure code examples work
