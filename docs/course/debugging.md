# Debugging Guide

Source: https://skaftenicki.github.io/dtu_mlops/s4_debugging_and_logging/debugging/

## Methods to Invoke Python Debugger

### 1. Direct Trace Method

Insert breakpoints manually in code:
```python
import pdb
pdb.set_trace()  # Execution stops here
```

Or use the built-in breakpoint:
```python
breakpoint()  # Python 3.7+
```

### 2. Editor Breakpoints (VS Code)

- Press `F9` to set inline breakpoints (visible as red dots)
- Press `F5` to start debugging
- Use the debug toolbar to navigate:
  - Continue (F5)
  - Step Over (F10)
  - Step Into (F11)
  - Step Out (Shift+F11)

### 3. Automatic Error Debugging

Launch scripts with automatic debugging on error:
```bash
python -m pdb -c continue my_script.py
```

The debugger starts automatically when the program encounters an error.

## Common ML Code Bugs

### Device Bugs
Tensors on mismatched devices (CPU vs GPU):
```python
# Bug
model = model.to("cuda")
data = data  # Still on CPU!
output = model(data)  # RuntimeError!

# Fix
data = data.to("cuda")
```

### Shape Bugs
Dimension mismatches in tensor operations:
```python
# Bug
x = torch.randn(32, 3, 28, 28)  # [N, C, H, W]
model = nn.Linear(28, 10)       # Expects flattened input
output = model(x)               # RuntimeError!

# Fix
x = x.view(32, -1)  # Flatten to [N, 784]
```

### Math Bugs
Incorrect mathematical implementations:
```python
# Bug: Using log_variance instead of variance
std = torch.exp(log_var)  # Wrong!

# Fix
std = torch.exp(0.5 * log_var)  # Correct: std = exp(log_var / 2)
```

### Training Bugs
Improper optimizer state management:
```python
# Bug: Missing gradient zeroing
for batch in dataloader:
    loss = model(batch)
    loss.backward()
    optimizer.step()  # Gradients accumulate!

# Fix
for batch in dataloader:
    optimizer.zero_grad()  # Clear gradients
    loss = model(batch)
    loss.backward()
    optimizer.step()
```

## PDB Commands

| Command | Action |
|---------|--------|
| `n` | Execute next line |
| `s` | Step into function |
| `c` | Continue execution |
| `q` | Quit debugger |
| `p <var>` | Print variable value |
| `pp <var>` | Pretty print variable |
| `l` | List source code |
| `w` | Print stack trace |
| `u` | Move up in stack |
| `d` | Move down in stack |

## Best Practices

1. Use structured debugging over random `print()` statements
2. Always maintain proper PyTorch training loop structure
3. Check tensor devices and shapes at critical points
4. Use assertions to catch bugs early:
   ```python
   assert x.shape == (batch_size, channels, height, width), f"Unexpected shape: {x.shape}"
   ```
5. Enable anomaly detection for gradient issues:
   ```python
   torch.autograd.set_detect_anomaly(True)
   ```
