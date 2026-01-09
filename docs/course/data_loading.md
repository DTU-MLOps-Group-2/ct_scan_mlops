# Distributed Data Loading Guide

Source: https://skaftenicki.github.io/dtu_mlops/s9_scalable_applications/data_loading/

## Core Principle

Data loading should never be the performance bottleneck. The goal is to ensure compute devices always have data ready.

## PyTorch DataLoader

### Basic Setup

```python
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, data_path):
        self.data_path = data_path
        self.files = os.listdir(data_path)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        # Load at runtime, not in __init__
        image = Image.open(self.files[idx])
        tensor = self.transform(image)
        return tensor, self.labels[idx]

dataloader = DataLoader(
    dataset,
    batch_size=32,
    num_workers=4,      # Parallel data loading
    shuffle=True,
    pin_memory=True     # Faster CPU→GPU transfer
)
```

### Key Parameters

| Parameter | Purpose |
|-----------|---------|
| `batch_size` | Samples per batch |
| `num_workers` | Parallel loading threads |
| `shuffle` | Randomize order each epoch |
| `pin_memory` | Use page-locked memory for GPU |
| `drop_last` | Drop incomplete final batch |
| `prefetch_factor` | Batches to prefetch per worker |

## Optimization Best Practices

### Worker Count

Test different values:

```python
import time

for num_workers in [0, 1, 2, 4, 8]:
    loader = DataLoader(dataset, batch_size=32, num_workers=num_workers)

    start = time.time()
    for _ in range(100):
        batch = next(iter(loader))
    elapsed = time.time() - start

    print(f"Workers: {num_workers}, Time: {elapsed:.2f}s")
```

### When More Workers Help

- Complex transforms/augmentations
- Slow disk I/O
- Large images requiring decompression
- Heavy preprocessing

### When More Workers Don't Help

- Fast lookups (data already in memory)
- Simple transforms
- Communication overhead exceeds benefit

### Platform-Specific Settings

```python
# Mac M1/M2
dataloader = DataLoader(
    dataset,
    num_workers=4,
    multiprocessing_context="fork"  # Required for Mac M1
)
```

### Pin Memory

```python
# When data fits in GPU memory
dataloader = DataLoader(
    dataset,
    pin_memory=True  # Accelerates CPU→GPU transfer
)
```

## Memory-Efficient Loading

### Don't Pre-load Everything

```python
# Bad: Loads all data into memory
class BadDataset(Dataset):
    def __init__(self, path):
        self.data = [load_image(f) for f in os.listdir(path)]

# Good: Load on demand
class GoodDataset(Dataset):
    def __init__(self, path):
        self.files = os.listdir(path)

    def __getitem__(self, idx):
        return load_image(self.files[idx])
```

### TensorDataset for Pre-processed Data

```python
from torch.utils.data import TensorDataset

# If data is already processed and fits in memory
dataset = TensorDataset(
    torch.tensor(images),
    torch.tensor(labels)
)
```

## Performance Measurement

```python
import time
from tqdm import tqdm

def benchmark_dataloader(loader, num_batches=100):
    start = time.time()
    for i, batch in enumerate(loader):
        if i >= num_batches:
            break
        # Simulate GPU transfer
        batch[0].cuda()
    return time.time() - start

# Compare configurations
for workers in [0, 2, 4, 8]:
    loader = DataLoader(dataset, batch_size=32, num_workers=workers)
    time_taken = benchmark_dataloader(loader)
    print(f"Workers={workers}: {time_taken:.2f}s")
```

## Best Practices

1. **Profile first**: Measure before optimizing
2. **Start with 4 workers**: Good default for most cases
3. **Use pin_memory=True** when using GPU
4. **Load at runtime**: Don't pre-load large datasets
5. **Match workers to CPU cores**: Don't exceed available cores
6. **Test on your hardware**: Optimal settings vary by system
