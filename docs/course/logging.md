# Logging Guide

Source: https://skaftenicki.github.io/dtu_mlops/s4_debugging_and_logging/logging/

## Application Logging

### Purpose

Recording events systematically to aid debugging, monitor application health, support auditing, and enable later analysis.

### Logging Levels (Hierarchical)

| Level | Purpose |
|-------|---------|
| DEBUG | Development-focused diagnostic information |
| INFO | General informational messages about program execution |
| WARNING | Alerts about potential issues (program continues functioning) |
| ERROR | Serious problems indicating failure in specific operations |
| CRITICAL | Severe failures potentially causing program termination |

### Loguru Package (Recommended)

Simplifies implementation dramatically:

```python
from loguru import logger

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

**Features**:
- Log level filtering without conditional statements
- File rotation capabilities (e.g., at 100 MB thresholds)
- Error catching via `logger.catch` decorator
- Customizable formatting and color output
- Lazy evaluation support via `opt` method

```python
# File rotation
logger.add("file.log", rotation="100 MB")

# Error catching
@logger.catch
def risky_function():
    return 1 / 0
```

### Logging vs Error Handling

- **Error handling** (try/except, raise): Modifies program flow at runtime
- **Logging**: Records post-execution information for inspection and analysis

---

## Experiment Logging (ML-Specific)

### Weights & Biases (Wandb)

**Setup**:
```bash
pip install wandb
wandb login  # Enter API key
```

**Basic Logging**:
```python
import wandb

wandb.init(project="my-project", config={
    "learning_rate": 0.001,
    "epochs": 10,
    "batch_size": 32
})

for epoch in range(epochs):
    wandb.log({
        "train_loss": train_loss,
        "val_loss": val_loss,
        "accuracy": accuracy
    })

wandb.finish()
```

**Advanced Artifact Logging**:
```python
# Images
wandb.log({"examples": wandb.Image(tensor, caption="Sample")})

# Histograms
wandb.log({"gradients": wandb.Histogram(grads)})

# Model checkpoints
artifact = wandb.Artifact("model", type="model")
artifact.add_file("model.pt")
wandb.log_artifact(artifact)
```

**Hyperparameter Sweeping**:

```yaml
# sweep.yaml
program: train.py
method: bayes
metric:
  name: val_loss
  goal: minimize
parameters:
  learning_rate:
    min: 0.0001
    max: 0.1
  batch_size:
    values: [16, 32, 64]
```

```bash
wandb sweep sweep.yaml
wandb agent <sweep_id>
```

**Model Registry**:
- Centralizes trained models as immutable artifacts
- Supports versioning and aliasing (e.g., "latest", "production", "staging")

### Docker Authentication

```bash
docker run -e WANDB_API_KEY=<key> image:tag
# Or
docker run --env-file .env image:tag
```

## Best Practices

1. Prefer structured logging tools over print statements
2. Configure appropriate log levels per audience
3. Implement log rotation to prevent file bloat
4. Store sensitive credentials (.env files) outside version control
5. Use experiment trackers for collaborative ML workflows
6. Log not just metrics but supporting artifacts
7. Maintain immutable model registries for reproducibility
