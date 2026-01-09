# Continuous Machine Learning (CML) Guide

Source: https://skaftenicki.github.io/dtu_mlops/s5_continuous_integration/cml/

## Core Concept

CML automates machine learning workflows beyond traditional CI/CD. It addresses ML-specific failure modes: data quality, model convergence, metric improvements, overfitting, and underfitting.

## MLOps Maturity Levels

| Level | Description |
|-------|-------------|
| 0-2 | Manual ML, basic versioning |
| 3 | Automated testing and monitoring |
| 4 | Continuous retraining and automated model updates |

## Data Pipeline Automation

### Trigger on Data Changes

```yaml
name: Data Pipeline

on:
  push:
    paths:
      - '*.dvc'
      - 'data.dvc'

jobs:
  data-stats:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: iterative/setup-dvc@v1

      - name: Pull data
        run: dvc pull

      - name: Generate statistics
        run: python scripts/data_stats.py > stats.md

      - name: Comment on PR
        uses: iterative/cml@v0.18
        run: cml comment create stats.md
```

### Generate Dataset Reports

```python
# scripts/data_stats.py
import pandas as pd

df = pd.read_csv('data/processed/train.csv')
print(f"# Dataset Statistics\n")
print(f"- Total samples: {len(df)}")
print(f"- Features: {df.shape[1]}")
print(f"- Class distribution:")
print(df['label'].value_counts().to_markdown())
```

## Model Staging & Deployment

### W&B Model Registry Webhook

```yaml
name: Model Staging

on:
  repository_dispatch:
    types: [staging]

jobs:
  test-model:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install wandb torch

      - name: Test model performance
        env:
          WANDB_API_KEY: ${{ secrets.WANDB_API_KEY }}
        run: |
          python scripts/test_model.py \
            --model-path ${{ github.event.client_payload.model_path }}

      - name: Promote to production
        if: success()
        run: |
          python scripts/promote_model.py \
            --model-path ${{ github.event.client_payload.model_path }}
```

### Performance Testing Pattern

```python
# scripts/test_model.py
import wandb
import torch
import time

def test_inference_speed(model, n_samples=100):
    x = torch.randn(1, 3, 224, 224)

    start = time.time()
    for _ in range(n_samples):
        with torch.no_grad():
            model(x)
    elapsed = time.time() - start

    avg_time = elapsed / n_samples
    assert avg_time < 0.1, f"Inference too slow: {avg_time:.3f}s"
    print(f"Average inference time: {avg_time:.3f}s")
```

## Critical Implementation Details

### Workflow Structure

1. Checkout code
2. Setup Python
3. Install dependencies
4. Authenticate with cloud storage (GCP/AWS)
5. Pull data via DVC
6. Execute ML-specific scripts
7. Publish results via CML

### CML Commands

```bash
# Comment on PR
cml comment create report.md

# Publish metrics
cml metrics add metrics.json

# Add images to report
cml image add confusion_matrix.png
```

## Best Practices

1. **Human oversight**: Maintain human review for high-stakes applications
2. **Staged rollouts**: Use staging aliases before production
3. **Performance gates**: Set clear thresholds for model promotion
4. **Data validation**: Always validate data before training
5. **Artifact tracking**: Version all models and datasets
6. **Rollback capability**: Maintain ability to revert to previous versions
