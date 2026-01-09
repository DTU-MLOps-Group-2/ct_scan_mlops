# CUDA-enabled training dockerfile for GPU training
# Base image with CUDA support (compatible with CUDA 12.4)
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Copenhagen

# Install Python 3.12 and build tools
RUN apt update && \
    apt install --no-install-recommends -y software-properties-common curl git && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt install --no-install-recommends -y python3.12 python3.12-venv python3.12-dev build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Install pip for Python 3.12
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

# Set python3.12 as default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

WORKDIR /app

# Copy project files
COPY pyproject.toml pyproject.toml
COPY src/ src/
COPY configs/ configs/
COPY LICENSE LICENSE
COPY README.md README.md

# Install PyTorch with CUDA support first
RUN --mount=type=cache,target=/root/.cache/pip pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

# Install the rest of the dependencies
RUN --mount=type=cache,target=/root/.cache/pip pip install .

ENTRYPOINT ["python", "-u", "-m", "ct_scan_mlops.train"]
CMD []
