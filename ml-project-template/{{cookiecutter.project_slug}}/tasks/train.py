"""Training, evaluation, and hyperparameter tuning tasks."""

import os

from invoke import Context, task

WINDOWS = os.name == "nt"
PROJECT_NAME = "{{ cookiecutter.project_slug }}"


@task
def train(ctx: Context, args: str = "") -> None:
    """Train model.

    Args:
        args: {% if cookiecutter.use_hydra == "yes" %}Hydra config overrides{% else %}Additional CLI arguments{% endif %}

    Examples:
        invoke train.train
        {%- if cookiecutter.use_hydra == "yes" %}
        invoke train.train --args "model=resnet train.max_epochs=100"
        invoke train.train --args "train.lr=0.001"
        {%- endif %}
    """
    ctx.run(f"uv run python -m {PROJECT_NAME}.train {args}", echo=True, pty=not WINDOWS)


@task
def evaluate(ctx: Context, checkpoint: str = "", args: str = "") -> None:
    """Evaluate a trained model.

    Args:
        checkpoint: Path to model checkpoint
        args: Additional arguments

    Examples:
        invoke train.evaluate --checkpoint outputs/model.ckpt
    """
    ckpt_arg = f"--checkpoint {checkpoint}" if checkpoint else ""
    ctx.run(f"uv run python -m {PROJECT_NAME}.evaluate {ckpt_arg} {args}", echo=True, pty=not WINDOWS)

{% if cookiecutter.use_wandb == "yes" %}

@task
def sweep(ctx: Context, sweep_config: str = "configs/sweeps/default.yaml", entity: str = "") -> None:
    """Create a W&B sweep from a config file.

    Args:
        sweep_config: Path to sweep YAML config
        entity: W&B entity (optional)

    Examples:
        invoke train.sweep
        invoke train.sweep --sweep-config configs/sweeps/custom.yaml
    """
    from pathlib import Path

    from loguru import logger

    sweep_path = Path(sweep_config)
    if not sweep_path.exists():
        logger.error(f"Sweep config not found: {sweep_config}")
        return

    cmd = f"uv run wandb sweep {sweep_config}"
    if entity:
        cmd += f" --entity {entity}"
    ctx.run(cmd, echo=True, pty=not WINDOWS)


@task
def sweep_agent(ctx: Context, sweep_id: str) -> None:
    """Run a W&B sweep agent.

    Args:
        sweep_id: Full sweep ID (ENTITY/PROJECT/SWEEP_ID)

    Examples:
        invoke train.sweep-agent --sweep-id entity/project/abc123
    """
    ctx.run(f"uv run wandb agent {sweep_id}", echo=True, pty=not WINDOWS)
{% endif %}
