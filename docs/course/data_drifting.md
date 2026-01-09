# Data Drift Monitoring Guide

Source: https://skaftenicki.github.io/dtu_mlops/s8_monitoring/data_drifting/

## Core Concept

Data drift occurs when model input data changes, leading to model performance degradation. Models trained on historical data may fail when receiving out-of-distribution inputs in production.

## Detection with Evidently

### Installation

```bash
pip install evidently scikit-learn pandas
```

### Basic Usage

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset

# Create report
report = Report(metrics=[
    DataDriftPreset(),
    DataQualityPreset()
])

# Run analysis
report.run(
    reference_data=training_data,    # Original training data
    current_data=production_data     # Recent production data
)

# Save report
report.save_html('drift_report.html')
```

### Detection Presets

| Preset | Purpose |
|--------|---------|
| `DataDriftPreset` | Monitor feature distribution changes |
| `DataQualityPreset` | Identify missing values, data quality issues |
| `TargetDriftPreset` | Track prediction label distribution shifts |
| `TextEvals` | Extract descriptive statistics from text data |

## Programmatic Testing

For CI/CD integration:

```python
from evidently.test_suite import TestSuite
from evidently.tests import (
    TestNumberOfMissingValues,
    TestShareOfDriftedColumns,
    TestColumnDrift
)

test_suite = TestSuite(tests=[
    TestNumberOfMissingValues(lte=0),
    TestShareOfDriftedColumns(lt=0.3),
    TestColumnDrift(column_name='feature_1')
])

test_suite.run(reference_data=ref_data, current_data=curr_data)
result = test_suite.as_dict()

if not result['summary']['all_passed']:
    raise Exception("Data drift detected!")
```

## Production Implementation

### Data Logging

```python
from fastapi import FastAPI, BackgroundTasks
import pandas as pd
from datetime import datetime

app = FastAPI()
predictions_log = []

def log_prediction(features, prediction):
    predictions_log.append({
        'timestamp': datetime.now(),
        'features': features,
        'prediction': prediction
    })

@app.post("/predict")
async def predict(data: dict, background_tasks: BackgroundTasks):
    prediction = model.predict(data['features'])
    background_tasks.add_task(log_prediction, data['features'], prediction)
    return {"prediction": prediction}
```

### Monitoring Service

```python
@app.get("/monitor")
async def monitor():
    # Get reference data
    reference = pd.read_csv('training_data.csv')

    # Get recent predictions
    current = pd.DataFrame(predictions_log[-1000:])

    # Run analysis
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current)

    return report.as_dict()
```

## Cloud Deployment Pattern

```
┌─────────────────┐
│  Prediction     │ → Logs predictions to Cloud Storage
│  Service        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cloud Storage  │ ← Stores prediction logs
│  Bucket         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Monitoring     │ → Fetches logs, runs Evidently
│  Service        │ → Returns HTML report
└─────────────────┘
```

## Limitations

**Marginal Distribution Testing**: Current tools analyze individual feature distributions. They cannot detect cases where marginal distributions remain unchanged while multivariate distributions shift.

For multivariate analysis, consider **Maximum Mean Discrepancy (MMD) tests**.

## Best Practices

1. **Multiple features**: Evaluate several features together when making retraining decisions
2. **Scheduled monitoring**: Run on production data segments regularly
3. **Unstructured data**: Extract quantitative features first (brightness, contrast for images; embeddings for text)
4. **Response strategy**: Establish clear drift thresholds triggering model retraining
5. **Baseline comparison**: Always compare against training data distribution
6. **Alert thresholds**: Set up automated alerts for significant drift
