# Boilerplate & PyTorch Lightning Guide

Source: https://skaftenicki.github.io/dtu_mlops/s4_debugging_and_logging/boilerplate/

## Core Concept

Boilerplate refers to standardized code that repeats across projects. In ML, this typically means training loops and utilities that divert focus from actual model development.

## PyTorch Lightning Framework

High-level framework that standardizes training workflows while maintaining flexibility.

### Key Components

#### LightningModule

Extends `nn.Module` with two essential methods:

```python
import pytorch_lightning as pl
import torch.nn as nn

class MyModel(pl.LightningModule):
    def __init__(self, hidden_size=256):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(784, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 10)
        )
        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.loss_fn(logits, y)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
```

#### Trainer

Handles training automation:

```python
from pytorch_lightning import Trainer

trainer = Trainer(max_epochs=10)
trainer.fit(model, train_dataloader)
```

### Key Trainer Arguments

| Flag | Purpose |
|------|---------|
| `max_epochs` | Training duration limit |
| `limit_train_batches` | Fraction of training data to use |
| `accelerator` | Device type ('gpu', 'cpu', 'auto') |
| `devices` | Number of devices to use |
| `precision` | Floating-point precision ('16-mixed', 'bf16-mixed') |
| `logger` | Logging integration (WandbLogger) |
| `callbacks` | List of callback objects |

### Data Integration

**Option 1: Methods in LightningModule**
```python
def train_dataloader(self):
    return DataLoader(train_dataset, batch_size=32)

def val_dataloader(self):
    return DataLoader(val_dataset, batch_size=32)
```

**Option 2: Pass directly to trainer**
```python
trainer.fit(model, train_dataloader, val_dataloader)
```

**Option 3: LightningDataModule**
```python
class MyDataModule(pl.LightningDataModule):
    def setup(self, stage):
        self.train_data = ...
        self.val_data = ...

    def train_dataloader(self):
        return DataLoader(self.train_data)
```

### Callbacks

Self-contained features added via the callbacks list:

```python
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping

checkpoint_callback = ModelCheckpoint(
    monitor='val_loss',
    mode='min',
    save_top_k=3
)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    mode='min'
)

trainer = Trainer(callbacks=[checkpoint_callback, early_stopping])
```

### Validation & Testing

```python
def validation_step(self, batch, batch_idx):
    x, y = batch
    logits = self(x)
    loss = self.loss_fn(logits, y)
    self.log('val_loss', loss, on_epoch=True)
    return loss

def test_step(self, batch, batch_idx):
    x, y = batch
    logits = self(x)
    acc = (logits.argmax(dim=1) == y).float().mean()
    self.log('test_acc', acc)
```

### Logging Integration

```python
# Scalar logging
self.log('train_loss', loss)

# Wandb integration
from pytorch_lightning.loggers import WandbLogger
logger = WandbLogger(project='my-project')
trainer = Trainer(logger=logger)

# Access raw wandb
self.logger.experiment.log({"image": wandb.Image(img)})
```

## Best Practices

1. Use `self.log()` for all metrics
2. Set `on_epoch=True` for validation metrics
3. Use callbacks for checkpointing and early stopping
4. Leverage automatic device placement
5. Use mixed precision for faster training
