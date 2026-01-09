# Configuration Management Guide

Source: https://skaftenicki.github.io/dtu_mlops/s3_reproducibility/config_files/

## Core Concepts

Reproducibility requires more than Docker—it demands systematic hyperparameter management. A study found that "Hyperparameters Specified" significantly impacts reproduction success.

## Configuration Approaches

### Basic Hardcoding (Problematic)

```python
class my_hp:
    batch_size: 64
    lr: 128
```

This loses experiment context without careful version control.

### Command-line Arguments (Better but Incomplete)

```bash
python train.py --batch_size 256 --learning_rate 1e-4
```

Still vulnerable to lost experiment records.

## Recommended Solution: Hydra + OmegaConf

Hydra provides YAML-based hierarchical configuration with automatic logging.

### Basic Setup

**config.yaml**:
```yaml
hyperparameters:
  batch_size: 64
  learning_rate: 1e-4
  epochs: 10
  seed: 42

model:
  type: cnn
  hidden_size: 256
```

**Loading via Hydra**:
```python
import hydra
from omegaconf import DictConfig

@hydra.main(config_path="configs", config_name="config", version_base=None)
def main(cfg: DictConfig):
    print(cfg.hyperparameters.batch_size)
    print(cfg.model.type)

if __name__ == "__main__":
    main()
```

### Command-line Overrides

```bash
python script.py hyperparameters.seed=1234
python script.py hyperparameters.batch_size=128 model.type=transformer
```

### Structured Config Directories

```
configs/
├── config.yaml           # Base configuration
├── model/
│   ├── cnn.yaml
│   └── transformer.yaml
├── training/
│   ├── default.yaml
│   └── large_batch.yaml
└── experiments/
    ├── exp1.yaml
    └── exp2.yaml
```

### Config Composition

```yaml
# config.yaml
defaults:
  - model: cnn
  - training: default

hyperparameters:
  seed: 42
```

### Object Instantiation

```python
from hydra.utils import instantiate

@dataclass
class ModelConfig:
    _target_: str
    hidden_size: int

# In config.yaml:
# model:
#   _target_: my_project.models.CNN
#   hidden_size: 256

model = instantiate(cfg.model)
```

## Best Practices

1. **Separate configurations from code** for version control
2. **Include random seeds** for full reproducibility
3. **Use structured config directories** for complex projects
4. **Enable command-line overrides** for experimentation
5. **Log via Python's logging module**, not print statements
6. **Leverage Hydra's instantiate feature** for object creation from configs

## Hydra Output Directory

Hydra automatically saves all configurations with experiment outputs:

```
outputs/
└── 2024-01-15/
    └── 10-30-45/
        ├── .hydra/
        │   ├── config.yaml
        │   ├── hydra.yaml
        │   └── overrides.yaml
        └── main.log
```

## Integration with Logging

```python
import logging

log = logging.getLogger(__name__)

@hydra.main(config_path="configs", config_name="config")
def main(cfg):
    log.info(f"Starting training with batch_size={cfg.hyperparameters.batch_size}")
```
