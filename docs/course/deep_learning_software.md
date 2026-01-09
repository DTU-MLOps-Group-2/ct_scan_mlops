# Deep Learning Software Guide

Source: https://skaftenicki.github.io/dtu_mlops/s1_development_environment/deep_learning_software/

## Framework Recommendations

**Dominant Frameworks**: TensorFlow, PyTorch, and JAX

PyTorch is the dominant framework for published models, research papers, and competition winners. It's the focus for this course due to its intuitive nature and research prevalence.

## PyTorch Best Practices

### Model Saving/Loading

**Recommended approach (weights only)**:
```python
# Save
torch.save(model.state_dict(), "model.pt")

# Load
model = MyModel()
model.load_state_dict(torch.load("model.pt"))
```

**Avoid** saving entire models with `torch.save(model, "model.pt")` as it can cause compatibility issues when modifying model definitions.

### Training Loop Essentials

Three critical function calls are required:
```python
optimizer.zero_grad()  # Prevents gradient accumulation
loss.backward()        # Calculates gradients
optimizer.step()       # Updates model weights
```

### Data Shape Requirements

Convolutional networks require input in `[N, C, H, W]` format:
- N: batch size (samples)
- C: channels
- H: height
- W: width

Use `.unsqueeze()` to add channel dimensions when needed.

## Hardware Acceleration

Move models and data to available accelerators:
```python
DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)

model = model.to(DEVICE)
data = data.to(DEVICE)
```

This supports:
- NVIDIA GPUs (CUDA)
- Apple Silicon (MPS)
- CPU fallback

## Code Organization

Separate concerns into distinct modules:

| File | Purpose |
|------|---------|
| `model.py` | Neural network architecture |
| `data.py` | Data loading and preprocessing |
| `train.py` | Training and evaluation logic |
| `evaluate.py` | Model evaluation on test sets |
| `visualize.py` | Feature extraction and visualization |

## Common Debugging Tips

- Always check tensor device placement (CPU vs GPU)
- Verify tensor shapes before operations
- Use `model.eval()` for inference mode
- Set `torch.manual_seed()` for reproducibility
