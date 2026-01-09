# Cloud Setup Guide (GCP)

Source: https://skaftenicki.github.io/dtu_mlops/s6_the_cloud/cloud_setup/

## Initial Account Setup

1. Create GCP account and obtain credits
2. Log into GCP Console
3. Verify billing status

## Project Creation

Create a new project (e.g., `dtumlops`) through the GCP console. Monitor creation progress via the notification bell.

## Google Cloud SDK Installation

### Installation

Follow the [official SDK guide](https://cloud.google.com/sdk/docs/install) for your operating system.

### Verification

```bash
gcloud -h
gcloud --version
```

## Authentication

### User Authentication

```bash
# Primary login
gcloud auth login

# For WSL users
gcloud auth login --no-launch-browser

# Application default credentials
gcloud auth application-default login
```

### Project Configuration

```bash
# Set default project
gcloud config set project <project-id>

# Verify configuration
gcloud config list
```

## Python API Setup

```bash
pip install --upgrade google-api-python-client
pip install google-cloud-storage
pip install google-cloud-aiplatform
```

## Enable Required APIs

```bash
# Cloud Functions
gcloud services enable cloudfunctions.googleapis.com

# Cloud Run
gcloud services enable run.googleapis.com

# Artifact Registry
gcloud services enable artifactregistry.googleapis.com

# Cloud Build
gcloud services enable cloudbuild.googleapis.com

# Vertex AI
gcloud services enable aiplatform.googleapis.com

# Secret Manager
gcloud services enable secretmanager.googleapis.com
```

## GPU Quota Configuration

1. Navigate to "IAM & Admin" → "Quotas"
2. Filter for GPU quotas
3. Request quota increase (typically 1-2 GPUs)

**Note**: Requests may be rejected within 24 hours of account creation.

## Service Account Creation

### Via Console

1. Go to "IAM & Admin" → "Service Accounts"
2. Create service account
3. Assign roles (minimal permissions)
4. Create and download JSON key

### Via CLI

```bash
# Create service account
gcloud iam service-accounts create my-service-account \
    --display-name="My Service Account"

# Assign roles
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:my-service-account@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectViewer"

# Create key
gcloud iam service-accounts keys create key.json \
    --iam-account=my-service-account@PROJECT_ID.iam.gserviceaccount.com
```

## Common Roles

| Role | Purpose |
|------|---------|
| `roles/storage.objectViewer` | Read Cloud Storage objects |
| `roles/storage.objectAdmin` | Full control of Storage objects |
| `roles/aiplatform.user` | Use Vertex AI services |
| `roles/run.invoker` | Invoke Cloud Run services |
| `roles/cloudbuild.builds.editor` | Submit Cloud Build jobs |

## Environment Variables

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

## Best Practices

1. Use service accounts for automation, not user accounts
2. Apply principle of least privilege
3. Rotate service account keys regularly
4. Store credentials securely (never in git)
5. Use Secret Manager for sensitive data
6. Enable audit logging for compliance
