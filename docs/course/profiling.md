# Profiling Guide

Source: https://skaftenicki.github.io/dtu_mlops/s4_debugging_and_logging/profiling/

## Core Profiling Questions

1. **Call Frequency**: How many times is each method in my code called?
2. **Execution Time**: How long do each of these methods take?

## cProfile Usage

Python's built-in profiler:

```bash
# Basic profiling
python -m cProfile myscript.py

# Sort by time
python -m cProfile -s time myscript.py

# Sort by cumulative time
python -m cProfile -s cumulative myscript.py

# Save to file
python -m cProfile -o profile.txt myscript.py
```

### Key Metrics

- `tottime`: Execution duration excluding subfunctions
- `cumtime`: Total duration including subfunctions
- `ncalls`: Number of calls

### Analysis with pstats

```python
import pstats

p = pstats.Stats('profile.txt')
p.sort_stats('cumulative').print_stats(10)
p.sort_stats('time').print_stats(10)
```

## PyTorch Profiler

For GPU/CPU operations:

```python
from torch.profiler import profile, ProfilerActivity

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
    model(inputs)

print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))
```

### Memory Profiling

```python
with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    profile_memory=True
) as prof:
    model(inputs)
```

### Visualization Options

**Chrome Tracing**:
```python
prof.export_chrome_trace("trace.json")
# View at chrome://tracing
```

**TensorBoard Integration**:
```python
from torch.profiler import tensorboard_trace_handler

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    on_trace_ready=tensorboard_trace_handler("./log_dir")
) as prof:
    for batch in dataloader:
        model(batch)
        prof.step()
```

## Performance Optimization Example

Common optimization: converting PIL image transforms to direct tensor operations:

```python
# Slow: PIL-based transforms
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])

# Faster: Pre-convert to tensors
dataset = TensorDataset(
    torch.tensor(images),
    torch.tensor(labels)
)
```

## Additional Tools

### line_profiler

For line-by-line profiling:
```bash
pip install line_profiler
kernprof -l -v script.py
```

### py-spy

For sampling profiler (minimal overhead):
```bash
pip install py-spy
py-spy top --pid <PID>
py-spy record -o profile.svg --pid <PID>
```

### memory_profiler

For memory usage analysis:
```bash
pip install memory_profiler
python -m memory_profiler script.py
```

## Best Practices

1. Profile before optimizing—measure, don't guess
2. Focus on hotspots that consume most time
3. Profile with representative data sizes
4. Compare before/after for validation
5. Use appropriate tool for the task:
   - `cProfile`: General Python profiling
   - `torch.profiler`: GPU/CUDA operations
   - `line_profiler`: Line-by-line analysis
   - `memory_profiler`: Memory usage
