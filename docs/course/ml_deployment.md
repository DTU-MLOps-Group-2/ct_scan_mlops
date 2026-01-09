# ML Deployment Patterns Guide

Source: https://skaftenicki.github.io/dtu_mlops/s7_deployment/ml_deployment/

## Model Export: ONNX

ONNX (Open Neural Network Exchange) enables framework-agnostic model deployment.

### Export PyTorch to ONNX

```python
import torch
import torch.onnx

model = MyModel()
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={
        'input': {0: 'batch_size'},
        'output': {0: 'batch_size'}
    }
)
```

### Validate Export

```python
import onnx
import numpy as np

# Verify model
onnx_model = onnx.load("model.onnx")
onnx.checker.check_model(onnx_model)

# Compare outputs
import onnxruntime as ort

ort_session = ort.InferenceSession("model.onnx")
ort_inputs = {'input': dummy_input.numpy()}
ort_outputs = ort_session.run(None, ort_inputs)

torch_outputs = model(dummy_input).detach().numpy()
np.testing.assert_allclose(torch_outputs, ort_outputs[0], rtol=1e-3, atol=1e-5)
```

### ONNX Runtime Inference

```python
import onnxruntime as ort

session = ort.InferenceSession(
    "model.onnx",
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
)

outputs = session.run(None, {'input': input_array})
```

## Dynamic Batching

Collect multiple requests and process together:

```python
# Using BentoML
import bentoml

@bentoml.service
class MyService:
    @bentoml.api(batchable=True, batch_dim=0, max_batch_size=32)
    def predict(self, inputs):
        return self.model(inputs)
```

## Service Composition

### Sequential Pipeline

```python
class Pipeline:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.model = Model()
        self.postprocessor = Postprocessor()

    def predict(self, input):
        x = self.preprocessor(input)
        x = self.model(x)
        return self.postprocessor(x)
```

### Ensemble Pattern

```python
class Ensemble:
    def __init__(self):
        self.models = [Model1(), Model2(), Model3()]

    def predict(self, input):
        outputs = [m(input) for m in self.models]
        return sum(outputs) / len(outputs)
```

## Model Serving Options

| Tool | Best For |
|------|----------|
| ONNX Runtime | Framework-agnostic, optimized inference |
| BentoML | Production services with batching |
| FastAPI | General APIs, custom logic |
| TorchServe | PyTorch-specific deployment |
| Triton | Multi-model serving, enterprise |

## Production Optimization

### Quantization

```python
import torch.quantization

# Dynamic quantization
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8
)
```

### Pruning

```python
import torch.nn.utils.prune as prune

# Global unstructured pruning
parameters_to_prune = [
    (model.layer1, 'weight'),
    (model.layer2, 'weight'),
]

prune.global_unstructured(
    parameters_to_prune,
    pruning_method=prune.L1Unstructured,
    amount=0.2,  # Remove 20% of weights
)
```

## Best Practices

1. **Architecture first**: Choose efficient architectures before optimization
2. **Benchmark**: Always measure actual inference time
3. **Validate exports**: Check ONNX outputs match PyTorch
4. **Use appropriate precision**: FP16/INT8 where possible
5. **Container optimization**: ONNX containers are 8.5x smaller than PyTorch
6. **Monitor in production**: Track latency and throughput
