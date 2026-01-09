# Command Line Interface (CLI) Guide

Source: https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/cli/

## Three CLI Methods

### 1. Project Scripts via pyproject.toml

Define executable entry points in your project configuration:

```toml
[project.scripts]
train = "my_project.train:main"
evaluate = "my_project.evaluate:main"
visualize = "my_project.visualize:main"
```

After installing with `pip install -e .`, commands become callable directly from the terminal.

### 2. Typer Framework

**Key requirement**: Type hints are necessary because Typer depends on them to function properly.

**Basic structure**:
```python
import typer
app = typer.Typer()

@app.command()
def hello(count: int = 1, name: str = "World"):
    for x in range(count):
        typer.echo(f"Hello {name}!")

if __name__ == "__main__":
    app()
```

**Subcommands pattern**:
```python
train_app = typer.Typer()
app.add_typer(train_app, name="train")

@train_app.command()
def svm(kernel: str = "linear"):
    pass

@train_app.command()
def neural_net(epochs: int = 10):
    pass
```

**Note**: Variables with underscores convert to hyphens in CLI (e.g., `n_neighbors` → `--n-neighbors`)

### 3. Invoke for Task Automation

Simplifies running complex terminal commands:

```python
from invoke import task

@task
def git(ctx, message):
    ctx.run("git add .")
    ctx.run(f"git commit -m '{message}'")
    ctx.run("git push")

@task
def setup(ctx):
    ctx.run("pip install -e .")
    ctx.run("dvc pull")
```

**Key context methods**:
- `ctx.run()` - Execute terminal commands
- `warn=True` - Continue on command failure
- `pty=True` - Run in pseudo-terminal
- `echo=True` - Print command before execution

## Typer Features

### Automatic Help

```bash
python script.py --help
python script.py train --help
```

### Optional vs Required Arguments

```python
@app.command()
def train(
    epochs: int,                    # Required (no default)
    lr: float = 0.001,             # Optional with default
    model: str = typer.Option(...) # Required option
):
    pass
```

### Enums for Choices

```python
from enum import Enum

class ModelType(str, Enum):
    cnn = "cnn"
    rnn = "rnn"
    transformer = "transformer"

@app.command()
def train(model_type: ModelType = ModelType.cnn):
    pass
```

## Best Practices

1. Provide single entry points rather than multiple scripts
2. Use consistent documentation (users can access help via `-h` flags)
3. Combine all three methods within the same project as needed
4. Consider Invoke for bootstrapping environments and data management tasks
5. Always add type hints for better error messages and autocomplete
