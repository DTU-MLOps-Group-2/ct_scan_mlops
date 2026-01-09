# Using the Cloud Guide (GCP)

Source: https://skaftenicki.github.io/dtu_mlops/s6_the_cloud/using_the_cloud/

## Compute Engine

### Create Virtual Machines

```bash
# Create basic VM
gcloud compute instances create my-vm \
    --zone=europe-west1-b \
    --machine-type=n1-standard-4

# Create with GPU
gcloud compute instances create gpu-vm \
    --zone=europe-west1-b \
    --machine-type=n1-standard-4 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --image-family=pytorch-latest-gpu \
    --image-project=deeplearning-platform-release
```

### Access and Manage VMs

```bash
# SSH into VM
gcloud compute ssh --zone europe-west1-b my-vm --project project-id

# Stop instance (avoid charges)
gcloud compute instances stop my-vm

# Delete instance
gcloud compute instances delete my-vm
```

### Deep Learning VMs

```bash
# List available images
gcloud compute images list \
    --project=deeplearning-platform-release \
    --no-standard-images
```

## Cloud Storage

### Create and Manage Buckets

```bash
# Create bucket
gsutil mb gs://my-bucket-name

# Enable versioning
gsutil versioning set on gs://my-bucket-name

# Upload files
gsutil cp file.txt gs://my-bucket-name/
gsutil cp -r folder/ gs://my-bucket-name/

# Download files
gsutil cp gs://my-bucket-name/file.txt .

# List contents
gsutil ls gs://my-bucket-name/
```

### DVC Integration

```bash
# Add GCS remote
dvc remote add -d remote_storage gs://my-bucket/dvc-data

# Enable versioning awareness
dvc remote modify remote_storage version_aware true

# Push/pull data
dvc push
dvc pull
```

### Access from VMs

Data is accessible at `/gcs/<bucket-name>/` on VMs with proper permissions.

## Artifact Registry

### Setup

```bash
# Enable APIs
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Create repository
gcloud artifacts repositories create my-repo \
    --repository-format=docker \
    --location=europe-west1
```

### Push Images

```bash
# Configure Docker
gcloud auth configure-docker europe-west1-docker.pkg.dev

# Tag image
docker tag my-image:latest \
    europe-west1-docker.pkg.dev/project-id/my-repo/my-image:latest

# Push
docker push europe-west1-docker.pkg.dev/project-id/my-repo/my-image:latest
```

### Cloud Build

`cloudbuild.yaml`:
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'europe-west1-docker.pkg.dev/$PROJECT_ID/my-repo/my-image:$COMMIT_SHA', '.']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'europe-west1-docker.pkg.dev/$PROJECT_ID/my-repo/my-image:$COMMIT_SHA']

images:
  - 'europe-west1-docker.pkg.dev/$PROJECT_ID/my-repo/my-image:$COMMIT_SHA'
```

## Vertex AI Training

### Enable Service

```bash
gcloud services enable aiplatform.googleapis.com
```

### Submit Custom Training Job

`config.yaml`:
```yaml
workerPoolSpecs:
  machineSpec:
    machineType: n1-standard-4
    acceleratorType: NVIDIA_TESLA_T4
    acceleratorCount: 1
  replicaCount: 1
  containerSpec:
    imageUri: europe-west1-docker.pkg.dev/project-id/repo/image:tag
    args:
      - --epochs=10
      - --batch_size=32
```

```bash
gcloud ai custom-jobs create \
    --region=europe-west1 \
    --display-name=my-training-job \
    --config=config.yaml
```

## Secrets Management

```bash
# Enable Secret Manager
gcloud services enable secretmanager.googleapis.com

# Create secret
echo -n "my-api-key" | gcloud secrets create my-secret --data-file=-

# Access secret
gcloud secrets versions access latest --secret=my-secret
```

### Use in Cloud Build

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    entrypoint: 'bash'
    args:
      - -c
      - |
        export API_KEY=$(gcloud secrets versions access latest --secret=my-secret)
        docker build --build-arg API_KEY=$API_KEY -t image .
```

## Cost Management

1. Always stop VMs when not in use
2. Use preemptible VMs for training
3. Set budget alerts
4. Clean up unused resources regularly
5. Use appropriate machine types
