# Distributed Training Guide

Source: https://skaftenicki.github.io/dtu_mlops/s9_scalable_applications/distributed_training/

## Training Paradigms

### Data Parallel (DP)

Basic multi-GPU training:

```python
from torch import nn

model = MyModel()
model = nn.DataParallel(model, device_ids=[0, 1])

# Training loop remains the same
for batch in dataloader:
    output = model(batch)
    loss = criterion(output, targets)
    loss.backward()
    optimizer.step()
```

**Process**:
1. Batch divided equally across devices
2. Model replicated to each device
3. Forward pass executed in parallel
4. Outputs collected on primary device
5. Gradients computed and scattered
6. Results reduced to main process

**Limitation**: Model replicas destroyed after each backward call, requiring repeated replication.

### Distributed Data Parallel (DDP)

Superior approach with persistent model copies:

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

# Initialize process group
dist.init_process_group("nccl")

# Wrap model
model = MyModel().to(device)
model = DDP(model, device_ids=[local_rank])

# Use DistributedSampler
sampler = torch.utils.data.distributed.DistributedSampler(dataset)
loader = DataLoader(dataset, sampler=sampler)

# Training loop
for epoch in range(epochs):
    sampler.set_epoch(epoch)
    for batch in loader:
        optimizer.zero_grad()
        output = model(batch)
        loss = criterion(output, targets)
        loss.backward()
        optimizer.step()
```

**Performance**: DDP achieves 2-3x faster performance compared to DP.

### Launch DDP Training

```bash
torchrun --nproc_per_node=2 train.py
```

## PyTorch Lightning

Simplified multi-GPU training:

```python
import pytorch_lightning as pl

class MyModel(pl.LightningModule):
    def training_step(self, batch, batch_idx):
        x, y = batch
        output = self(x)
        loss = self.criterion(output, y)
        return loss

trainer = pl.Trainer(
    accelerator='gpu',
    devices=2,
    strategy='ddp'
)

trainer.fit(model, dataloader)
```

### Strategy Options

| Strategy | Use Case |
|----------|----------|
| `ddp` | Multi-GPU, single node |
| `ddp_spawn` | Multi-GPU with spawning |
| `deepspeed` | Large models, ZeRO optimization |
| `fsdp` | Fully Sharded Data Parallel |

## Mixed Precision Training

```python
# PyTorch
scaler = torch.cuda.amp.GradScaler()

for batch in dataloader:
    optimizer.zero_grad()
    with torch.cuda.amp.autocast():
        output = model(batch)
        loss = criterion(output, targets)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()

# Lightning
trainer = pl.Trainer(precision='16-mixed')
```

## Best Practices

1. **Communication overhead**: Minimize data transfers between devices
2. **Batch size**: Scale with number of GPUs (effective_batch = batch × num_gpus)
3. **Learning rate**: Scale with batch size (linear scaling rule)
4. **Gradient synchronization**: Happens automatically in DDP
5. **Benchmarking**: Perfect 2x speedup unrealistic due to communication

## Scaling Expectations

| GPUs | Expected Speedup | Notes |
|------|------------------|-------|
| 1 | 1.0x | Baseline |
| 2 | ~1.8x | Some overhead |
| 4 | ~3.5x | More overhead |
| 8 | ~6-7x | Diminishing returns |

## Common Issues

### Memory Errors

```python
# Reduce batch size per GPU
batch_per_gpu = total_batch // num_gpus
```

### Gradient Accumulation

```python
# Accumulate over multiple steps
accumulation_steps = 4

for i, batch in enumerate(dataloader):
    loss = model(batch) / accumulation_steps
    loss.backward()

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```
