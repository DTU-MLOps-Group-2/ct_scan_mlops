# Unit Testing Guide

Source: https://skaftenicki.github.io/dtu_mlops/s5_continuous_integration/unittesting/

## Core Testing Framework

**Pytest** is the recommended testing framework for Python projects.

### Naming Conventions
- Test files: `test_*.py`
- Test functions: `test_*`

### Installation and Running

```bash
pip install pytest
pytest tests/           # Run all tests
pytest tests/test_data.py  # Run specific file
pytest -v               # Verbose output
pytest -x               # Stop on first failure
```

## Test Organization

### File Structure

```
tests/
├── __init__.py
├── test_data.py
├── test_model.py
└── test_training.py
```

### Path Utilities (`tests/__init__.py`)

```python
import os
_TEST_ROOT = os.path.dirname(__file__)
_PROJECT_ROOT = os.path.dirname(_TEST_ROOT)
_PATH_DATA = os.path.join(_PROJECT_ROOT, "data")
```

## Test Categories

### Data Testing (`test_data.py`)

```python
import pytest
from tests import _PATH_DATA

def test_dataset_length():
    dataset = MyDataset(_PATH_DATA)
    assert len(dataset) == 1000

def test_sample_shape():
    dataset = MyDataset(_PATH_DATA)
    x, y = dataset[0]
    assert x.shape == (1, 28, 28)

def test_all_labels_present():
    dataset = MyDataset(_PATH_DATA)
    labels = [y for _, y in dataset]
    assert set(labels) == set(range(10))
```

### Model Testing (`test_model.py`)

```python
import torch
import pytest
from src.model import MyModel

def test_model_output_shape():
    model = MyModel()
    x = torch.randn(32, 1, 28, 28)
    output = model(x)
    assert output.shape == (32, 10)

def test_model_invalid_input():
    model = MyModel()
    x = torch.randn(32, 3)  # Wrong shape
    with pytest.raises(RuntimeError):
        model(x)
```

## Key Pytest Features

### Parametrization

Test multiple inputs efficiently:

```python
@pytest.mark.parametrize("batch_size", [1, 32, 64])
def test_model_batch_sizes(batch_size: int):
    model = MyModel()
    x = torch.randn(batch_size, 1, 28, 28)
    output = model(x)
    assert output.shape[0] == batch_size
```

### Skip Decorator

Conditionally skip tests:

```python
@pytest.mark.skipif(
    not os.path.exists(_PATH_DATA),
    reason="Data files not found"
)
def test_data_loading():
    pass
```

### Fixtures

Reusable test components:

```python
@pytest.fixture
def model():
    return MyModel()

@pytest.fixture
def sample_batch():
    return torch.randn(32, 1, 28, 28)

def test_forward(model, sample_batch):
    output = model(sample_batch)
    assert output.shape == (32, 10)
```

### Error Testing

Verify exceptions raise appropriately:

```python
def test_invalid_input_raises():
    model = MyModel()
    with pytest.raises(ValueError, match='Expected input to be a 4D tensor'):
        model(torch.randn(1, 2, 3))
```

## Code Coverage

```bash
pip install coverage

# Run with coverage
coverage run -m pytest tests/

# Generate reports
coverage report
coverage report -m  # Show missing lines
coverage html       # HTML report
```

### Configuration in `pyproject.toml`

```toml
[tool.coverage.run]
omit = ["tests/*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## ML Testing Considerations

Testing ML systems differs from traditional software:

1. **Data Testing**: Verify data distributions and quality
2. **Model Testing**: Check shapes, outputs, and error handling
3. **Training Testing**: Ensure scripts run without errors
4. **Integration Testing**: Test end-to-end pipelines
5. **Data Drift Monitoring**: Track distribution shifts in production
