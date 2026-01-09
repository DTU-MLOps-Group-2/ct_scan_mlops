# Docker Image Optimization Guide

Source: https://devopscube.com/reduce-docker-image-size/

## Six Core Optimization Methods

### 1. Use Minimal Base Images
- **Alpine images** are recommended as they're as small as 5.59MB
- Alpine images come with a shell for debugging
- **Distroless images** from Google provide even more stripped-down versions for Java, Node.js, Python, and Rust
- Distroless images lack shells entirely but offer better security
- Most distributions now have minimal base images available

**Example:**
```dockerfile
# Alpine variant
FROM python:3.12-alpine

# Distroless variant (production)
FROM gcr.io/distroless/python3
```

### 2. Implement Multistage Builds
- Use intermediate images for compilation and dependencies
- Copy only necessary files to a lighter runtime image
- Can reduce image size by **over 80%**
- Example: Node.js application reduced from 910MB to 171MB
- Further reduction to 118MB possible with distroless images

**Example:**
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage - much smaller
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/main.js"]
```

### 3. Minimize Layer Count
- Each `RUN`, `COPY`, and `FROM` instruction creates a layer
- Combining commands reduces layers and improves performance
- Example: Combining 5 separate RUN statements into 1 reduced:
  - Build time from 117.1s to 91.7s
  - Image size from 227MB to 216MB

**Bad - Multiple layers:**
```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get clean
```

**Good - Single layer:**
```dockerfile
RUN apt-get update && \
    apt-get install -y curl git vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 4. Leverage Docker Caching
- Place frequently-changing instructions (like COPY) after stable ones
- Allows Docker to reuse cached layers during rebuilds
- Order matters: dependencies → configuration → code

**Example:**
```dockerfile
FROM python:3.12-slim

# Rarely changes - cached
COPY requirements.txt .
RUN pip install -r requirements.txt

# Changes frequently - put last
COPY src/ src/
```

### 5. Configure .dockerignore
- Exclude unnecessary files to reduce image size
- Prevent cache invalidation from unrelated changes
- Similar to .gitignore but for Docker builds

**Example .dockerignore:**
```
.git
.gitignore
*.md
.venv
__pycache__
*.pyc
.pytest_cache
.coverage
tests/
docs/
node_modules/
```

### 6. Store Data Externally
- Keep application data separate using container volumes
- Don't bundle data in the image
- Use data version control systems like DVC

**Bad:**
```dockerfile
COPY large_dataset/ /app/data/
```

**Good:**
```dockerfile
# Data pulled at runtime via DVC or mounted as volume
VOLUME /app/data
```

## Practical Commands

### Building with BuildKit (Recommended)
```bash
export DOCKER_BUILDKIT=1
docker build -t image-name --no-cache -f Dockerfile .
```

### Checking Image Size
```bash
docker image ls
docker history <image-name>
```

## Recommended Tools

### Dive
Layer exploration tool for optimization analysis
```bash
dive <image-name>
```

### SlimToolkit
Claims up to 30x size reduction
```bash
slim build <image-name>
```

### Docker Squash
Compresses multiple layers into one
```bash
docker build --squash -t <image-name> .
```

## Additional Best Practices

### Use Specific Tags
```dockerfile
# Good
FROM python:3.12-slim

# Bad
FROM python:latest
```

### Clean Up in Same Layer
```dockerfile
RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### Use --no-cache-dir with pip
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

## Performance Metrics

- **Multistage builds**: 80%+ size reduction possible
- **Layer combining**: 20-30% build time improvement
- **Alpine vs full images**: 95%+ size reduction (5MB vs 100MB+)
- **Proper caching**: Rebuild time from minutes to seconds
