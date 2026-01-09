# Docker Instructions - DTU MLOps Course

Source: https://skaftenicki.github.io/dtu_mlops/s3_reproducibility/docker/

## Core Concepts

Docker provides **system-level reproducibility** by capturing:
- Operating system
- Software dependencies
- Application code

in isolated, portable containers.

### Three Main Components

1. **Dockerfile**: Text file containing commands to build an application
2. **Docker Image**: Standalone executable package with all dependencies
3. **Docker Container**: Running instance of an image

## Essential Docker Commands

### Installation & Testing
```bash
docker run hello-world                    # Test Docker installation
```

### Image Management
```bash
docker pull busybox                       # Download image from registry
docker images                             # List all local images
docker rmi <image_id>                     # Remove image
```

### Container Management
```bash
docker ps                                 # Show running containers
docker ps -a                              # Show all containers (running + stopped)
docker rm <container_id>                  # Remove container
docker stop <container_id>                # Stop running container
```

### Building Images
```bash
docker build -f train.dockerfile . -t train:latest
```
- `-f`: Specify Dockerfile name
- `.`: Build context (current directory)
- `-t`: Tag the image with name:version

### Running Containers
```bash
docker run --name experiment1 train:latest
```

Common flags:
- `--name`: Assign name to container
- `--rm`: Automatically remove container after execution
- `-it`: Interactive terminal mode
- `-v`: Mount volume between host and container
- `--gpus all`: Enable GPU access

### File Operations
```bash
docker cp {container}:{path} {local_path}   # Copy files from container
```

## Dockerfile Structure

### Basic Template
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

# Copy application code
COPY src/ src/

# Install application
RUN pip install . --no-deps --no-cache-dir

# Set entrypoint
ENTRYPOINT ["python", "-u", "src/<project>/train.py"]
```

### Dockerfile Instructions

- `FROM`: Base image to build upon
- `RUN`: Execute commands in the container
- `COPY`: Copy files from host to container
- `WORKDIR`: Set working directory
- `ENTRYPOINT`: Default executable when container starts
- `CMD`: Default arguments to ENTRYPOINT (can be overridden)

## Best Practices

### 1. Layer Caching
Structure Dockerfiles to separate dependency installation from application code.

**Key insight:** "Docker can cache our project dependencies separately from our application code"

**Good order:**
```dockerfile
COPY requirements.txt requirements.txt     # Rarely changes
RUN pip install -r requirements.txt        # Cached layer

COPY src/ src/                             # Changes frequently
```

This avoids reinstalling dependencies when only code changes.

### 2. Reduce Image Size
- Use `--no-cache-dir` with pip
- Clean up package manager caches
- Use minimal base images (e.g., `-slim`, `-alpine`)
- Combine RUN commands to reduce layers

### 3. Use .dockerignore
Exclude unnecessary files from build context:
```
__pycache__/
*.pyc
.git/
.venv/
tests/
.coverage
```

## Volume Mounting

Share files between host and container:

**Windows:**
```bash
docker run --name container_name -v %cd%/models:/models/ image:latest
```

**Linux/Mac:**
```bash
docker run --name container_name -v $(pwd)/models:/models/ image:latest
```

This mounts the local `models/` directory to `/models/` in the container.

## GPU Support

### Using NVIDIA GPUs

1. **Use NVIDIA base image:**
```dockerfile
FROM nvcr.io/nvidia/pytorch:22.07-py3
```

2. **Run with GPU access:**
```bash
docker run --gpus all image:latest
```

**Prerequisites:**
- NVIDIA GPU
- NVIDIA drivers installed
- NVIDIA Container Toolkit installed

## Data Version Control (DVC) Integration

Include DVC in Dockerfile to pull data at build time:

```dockerfile
RUN dvc init --no-scm
COPY .dvc/config .dvc/config
COPY *.dvc ./
RUN dvc config core.no_scm true
RUN dvc pull
```

**Note:** This embeds credentials in the image. For production, use runtime data pulling or BuildKit secrets.

## Platform-Specific Considerations

### Mac M1/M2 (ARM Architecture)

Specify platform when building and running:

```bash
docker build --platform linux/amd64 -f train.dockerfile . -t train:latest
docker run --platform linux/amd64 train:latest
```

This ensures compatibility when deploying to x86_64 cloud servers.

## Advanced Techniques

### Multi-stage Builds
Use for separating build and runtime dependencies (see docker_Opt.md).

### BuildKit Cache Mounts
Leverage BuildKit for faster rebuilds:
```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
```

### Environment Variables
```dockerfile
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
```

## Common Patterns

### Development vs Production
- **Development**: Use `-slim` images, include debugging tools
- **Production**: Use distroless or minimal images, exclude dev dependencies

### Entrypoint vs CMD
- **ENTRYPOINT**: Fixed command (e.g., `python app.py`)
- **CMD**: Default arguments (can be overridden at runtime)

```dockerfile
ENTRYPOINT ["python", "-u", "src/train.py"]
CMD ["--epochs", "5"]
```

Run with custom epochs:
```bash
docker run image:latest --epochs 10
```

## Troubleshooting

### Container Exits Immediately
- Check logs: `docker logs <container_id>`
- Run interactively: `docker run -it image:latest /bin/bash`

### Permission Denied
- Check file permissions in COPY commands
- Ensure execute permissions: `RUN chmod +x script.sh`

### Build Context Too Large
- Add files to `.dockerignore`
- Build from specific directory context

## Summary

Docker ensures reproducibility by:
1. Capturing exact OS and dependencies
2. Providing isolation from host system
3. Creating portable, shareable environments
4. Enabling consistent builds across different machines

**Key principle:** Structure Dockerfiles to maximize caching efficiency and minimize image size.
