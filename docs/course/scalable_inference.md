# Scalable Inference Guide

Source: https://skaftenicki.github.io/dtu_mlops/s9_scalable_applications/inference/

## Core Objective

Optimize inference for production: reduce model size, improve speed, enable edge deployment.

## Optimization Strategies

### 1. Architecture Selection (Highest Impact)

Choose efficient architectures first:

```python
import torch
from ptflops import get_model_complexity_info

model = MyModel()
flops, params = get_model_complexity_info(
    model,
    (3, 224, 224),
    as_strings=True
)
print(f"FLOPs: {flops}, Params: {params}")
```

**Key insight**: Convolutional models generally outperform transformers for equivalent parameter counts.

### 2. Quantization

Convert 32-bit floats to integers:

```python
import torch.quantization

# Dynamic quantization (easiest)
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear, torch.nn.LSTM},
    dtype=torch.qint8
)

# Static quantization (better performance)
model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
model_prepared = torch.quantization.prepare(model)
# Calibrate with representative data
for batch in calibration_loader:
    model_prepared(batch)
model_quantized = torch.quantization.convert(model_prepared)
```

**Benefits**:
- 4x memory transfer speed improvements
- 75% storage reduction
- Faster integer operations

### 3. Pruning

Remove low-magnitude weights:

```python
import torch.nn.utils.prune as prune

# Local pruning (per layer)
prune.l1_unstructured(model.layer1, name='weight', amount=0.3)

# Global pruning (across network)
parameters_to_prune = [
    (model.layer1, 'weight'),
    (model.layer2, 'weight'),
    (model.layer3, 'weight'),
]

prune.global_unstructured(
    parameters_to_prune,
    pruning_method=prune.L1Unstructured,
    amount=0.2  # Remove 20% of weights
)

# Make permanent
prune.remove(model.layer1, 'weight')
```

### 4. Knowledge Distillation

Compress large models into smaller ones:

```python
def distillation_loss(student_logits, teacher_logits, labels, temperature=3.0, alpha=0.5):
    # Soft targets from teacher
    soft_loss = F.kl_div(
        F.log_softmax(student_logits / temperature, dim=1),
        F.softmax(teacher_logits / temperature, dim=1),
        reduction='batchmean'
    ) * (temperature ** 2)

    # Hard targets
    hard_loss = F.cross_entropy(student_logits, labels)

    return alpha * soft_loss + (1 - alpha) * hard_loss

# Training loop
for batch, labels in dataloader:
    with torch.no_grad():
        teacher_logits = teacher_model(batch)

    student_logits = student_model(batch)
    loss = distillation_loss(student_logits, teacher_logits, labels)
    loss.backward()
    optimizer.step()
```

## ONNX Optimization

```python
import onnxruntime as ort
from onnxruntime.transformers import optimizer

# Optimize ONNX model
optimized_model = optimizer.optimize_model(
    "model.onnx",
    model_type='bert',
    opt_level=2
)
optimized_model.save_model_to_file("model_optimized.onnx")

# Use optimized runtime
session = ort.InferenceSession(
    "model_optimized.onnx",
    providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider']
)
```

## Benchmarking

```python
import time
import torch

def benchmark_model(model, input_shape, num_runs=100):
    model.eval()
    x = torch.randn(input_shape)

    # Warmup
    for _ in range(10):
        with torch.no_grad():
            model(x)

    # Benchmark
    if torch.cuda.is_available():
        torch.cuda.synchronize()

    start = time.time()
    for _ in range(num_runs):
        with torch.no_grad():
            model(x)

    if torch.cuda.is_available():
        torch.cuda.synchronize()

    avg_time = (time.time() - start) / num_runs
    print(f"Average inference time: {avg_time*1000:.2f}ms")
    return avg_time
```

## Best Practices

1. **Architecture first**: Yields largest speed gains
2. **Benchmark everything**: Measure actual improvements
3. **Combine techniques**: Quantization + pruning often works well
4. **Validate accuracy**: Check model quality after optimization
5. **Hardware-specific**: Optimize for target deployment platform
6. **Profile bottlenecks**: Use torch.profiler to identify issues
