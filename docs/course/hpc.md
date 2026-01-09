# High Performance Clusters (HPC) Guide

Source: https://skaftenicki.github.io/dtu_mlops/s10_extra/high_performance_clusters/

## Cluster Architecture

### Supercomputers

- Organized into modules (CPU, GPU, RAM, storage)
- Connected by network links
- Best for resource-intensive applications requiring inter-device communication

### Load Sharing Facility (LSF)

- Network of independent computers
- Each node has own resources
- Preferable when needs fit within single node

## Key Components

### HPC Scheduler

Manages job queue and resource allocation. Major systems:

- **SLURM**: Most common
- **PBS/MOAB**: Alternative systems
- **LSF**: IBM's scheduler

## Environment Setup

### Install Conda/Miniconda

```bash
# Download miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Create environment
conda create -n hpc_env python=3.10 --no-default-packages
conda activate hpc_env

# Install requirements
pip install -r requirements.txt
```

## SLURM Job Submission

### Basic Job Script (`job.sh`)

```bash
#!/bin/bash
#SBATCH --job-name=training
#SBATCH --output=output_%j.log
#SBATCH --error=error_%j.log
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:1

# Load modules
module load cuda/12.1
module load python/3.10

# Activate environment
source activate hpc_env

# Run training
python train.py --epochs 100
```

### Submit Job

```bash
sbatch job.sh
```

### Common SLURM Commands

| Command | Purpose |
|---------|---------|
| `sbatch script.sh` | Submit job |
| `squeue -u $USER` | Check job status |
| `scancel <job_id>` | Cancel job |
| `sinfo` | Show cluster status |
| `sacct -j <job_id>` | Job accounting info |

## GPU Jobs

### Request GPU Resources

```bash
#SBATCH --partition=gpu
#SBATCH --gres=gpu:v100:2  # 2 V100 GPUs
```

### Load CUDA

```bash
module load cuda/12.1
module load cudnn/8.6
```

### Multi-GPU Training

```bash
#!/bin/bash
#SBATCH --gres=gpu:4
#SBATCH --ntasks-per-node=4

srun python -m torch.distributed.launch \
    --nproc_per_node=4 \
    train.py
```

## Interactive Sessions

```bash
# Request interactive GPU session
srun --partition=gpu --gres=gpu:1 --time=01:00:00 --pty bash

# Or with salloc
salloc --partition=gpu --gres=gpu:1 --time=01:00:00
```

## Array Jobs

Run multiple experiments:

```bash
#!/bin/bash
#SBATCH --array=0-9

# Each task gets different SLURM_ARRAY_TASK_ID
python train.py --seed $SLURM_ARRAY_TASK_ID
```

## Best Practices

1. **Test locally first**: Debug before submitting to queue
2. **Request appropriate resources**: Don't over-request
3. **Use checkpointing**: Save progress for long jobs
4. **Monitor jobs**: Check output files during execution
5. **Clean up**: Remove large temporary files
6. **Use scratch space**: For temporary large files
7. **Batch similar jobs**: Use array jobs for hyperparameter sweeps

## Common Issues

### Job Pending

- Check queue: `squeue`
- Check resources: `sinfo`
- Reduce resource request

### Out of Memory

```bash
#SBATCH --mem=64G  # Increase memory
```

### GPU Not Found

```bash
# Ensure CUDA is loaded
module load cuda/12.1

# Check GPU visibility
nvidia-smi
```

## Environment Modules

```bash
# List available modules
module avail

# Load module
module load python/3.10

# Show loaded modules
module list

# Unload module
module unload python
```
