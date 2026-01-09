# Cloud Deployment Guide

Source: https://skaftenicki.github.io/dtu_mlops/s7_deployment/cloud_deployment/

## Cloud Functions

Simplest way to deploy single-script applications.

### Setup

```bash
gcloud services enable cloudfunctions.googleapis.com
```

### Function Structure

```python
import functions_framework
from google.cloud import storage
import pickle

# Load model at startup
storage_client = storage.Client()
bucket = storage_client.bucket("my-bucket")
blob = bucket.blob("model.pkl")
model = pickle.loads(blob.download_as_string())

@functions_framework.http
def predict(request):
    data = request.get_json()
    prediction = model.predict([data["features"]])
    return {"prediction": prediction.tolist()}
```

### Deployment

```bash
gcloud functions deploy predict \
    --gen2 \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated \
    --region europe-west1
```

## Cloud Run

Deploy containerized applications with full flexibility.

### Dockerfile Requirements

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Important: Listen on PORT environment variable
EXPOSE $PORT
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Deployment Steps

```bash
# Build and push image
docker build -t gcr.io/PROJECT_ID/my-app .
docker push gcr.io/PROJECT_ID/my-app

# Deploy to Cloud Run
gcloud run deploy my-service \
    --image gcr.io/PROJECT_ID/my-app \
    --region europe-west1 \
    --allow-unauthenticated \
    --memory 2Gi
```

### Environment Variables

```bash
gcloud run deploy my-service \
    --set-env-vars "MODEL_PATH=/models/model.pt,DEBUG=false"
```

## Continuous Deployment

`cloudbuild.yaml`:

```yaml
steps:
  # Build
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA', '.']

  # Push
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA']

  # Deploy
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'my-service'
      - '--image'
      - 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA'
      - '--region'
      - 'europe-west1'
```

### Create Trigger

```bash
gcloud builds triggers create github \
    --repo-name=my-repo \
    --repo-owner=my-org \
    --branch-pattern=^main$ \
    --build-config=cloudbuild.yaml
```

## Storage Integration

### Mount Cloud Storage

```bash
gcloud run services update my-service \
    --add-volume name=models,type=cloud-storage,bucket=my-bucket \
    --add-volume-mount volume=models,mount-path="/models"
```

### Secrets Management

```bash
# Create secret
echo -n "api-key-value" | gcloud secrets create my-api-key --data-file=-

# Use in Cloud Run
gcloud run deploy my-service \
    --update-secrets=API_KEY=my-api-key:latest
```

## Production Patterns

### Memory Configuration

For large ML models, increase container memory:

```bash
gcloud run deploy my-service \
    --memory 4Gi \
    --cpu 2
```

### Concurrency Settings

```bash
gcloud run deploy my-service \
    --concurrency 1  # For ML models that aren't thread-safe
```

### Health Checks

```python
@app.get("/health")
def health():
    return {"status": "healthy"}
```

## Best Practices

1. Use Cloud Run for complex applications, Functions for simple ones
2. Always set memory limits appropriate for your model
3. Implement health check endpoints
4. Use Secret Manager for credentials
5. Enable continuous deployment for production
6. Monitor via Cloud Logging and Monitoring
