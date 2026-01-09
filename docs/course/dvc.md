# Data Version Control (DVC) Guide

Source: https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/dvc/

## Core Concept

DVC extends Git to version control large artifacts like datasets and models. Rather than storing massive files, DVC maintains small metafiles that point to remote storage locations.

## Installation

```bash
pip install dvc
pip install dvc-gdrive  # For Google Drive
pip install dvc-gs      # For Google Cloud Storage
pip install dvc-s3      # For AWS S3
```

Optional: Install all backends with `pip install dvc[all]`

## Setup Sequence

1. **Initialize DVC**: `dvc init`
2. **Configure Remote Storage**: `dvc remote add -d storage <remote-url>`
3. **Track Data**: `dvc add data/`
4. **Commit Metafiles**: `git add .dvc/config data.dvc .gitignore`
5. **Push Data**: `dvc push` (requires authentication)

## Key Commands

| Task | Command |
|------|---------|
| Initialize DVC | `dvc init` |
| Add files to DVC | `dvc add <path>` |
| Push data remotely | `dvc push` |
| Pull data locally | `dvc pull` |
| Check status | `dvc status` |
| Revert to version | `git checkout <tag>` + `dvc checkout` |

## Remote Storage Configuration

### Google Cloud Storage
```bash
dvc remote add -d remote_storage gs://bucket-name/path
dvc remote modify remote_storage version_aware true
```

### Google Drive
```bash
dvc remote add -d storage gdrive://<folder-id>
```

### AWS S3
```bash
dvc remote add -d remote_storage s3://bucket-name/path
```

## Data Versioning Workflow

```
dvc add → git add → git commit → git tag → dvc push → git push
```

## Best Practices for Large Datasets

- **Multiple Small Files**: Archive into single `.zip` file, store in `data/raw/`, unzip to `data/processed/`
- **Tabular Data**: Convert to `.parquet` or `.csv` format for single-file storage
- **Repository Verification**: Check for `.dvc/` folder or run `dvc status`

## Cloning Repository with Data

```bash
git clone <repository>
cd <repository>
dvc pull
```

## Docker Integration

For build-time data pulling:
```dockerfile
RUN dvc init --no-scm
COPY .dvc/config .dvc/config
COPY *.dvc ./
RUN dvc config core.no_scm true
RUN dvc pull
```

For runtime data pulling (recommended):
```dockerfile
RUN dvc init --no-scm
COPY .dvc/config .dvc/config
COPY *.dvc ./
RUN dvc config core.no_scm true
# Pull at runtime via entrypoint
```

## Important Notes

- Google Drive API authentication changed August 2024, requiring custom Google Cloud project setup
- Use `.dvc` files as metafiles tracked by git
- Never commit actual data files to git
- Always add data directories to `.gitignore`
