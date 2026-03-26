"""Model evaluation utilities."""

from pathlib import Path

import pytorch_lightning as pl
import torch
from loguru import logger

from {{ cookiecutter.project_slug }}.data import DataModule
from {{ cookiecutter.project_slug }}.model import SimpleCNN


def evaluate_model(checkpoint: str, data_dir: str = "data") -> dict:
    """Evaluate a trained model checkpoint.

    Args:
        checkpoint: Path to model checkpoint file
        data_dir: Path to data directory

    Returns:
        Dictionary of evaluation metrics
    """
    ckpt_path = Path(checkpoint)
    if not ckpt_path.exists():
        logger.error(f"Checkpoint not found: {checkpoint}")
        return {}

    logger.info(f"Loading model from {checkpoint}")
    model = SimpleCNN.load_from_checkpoint(checkpoint)

    datamodule = DataModule(data_dir=data_dir)
    datamodule.setup(stage="test")

    trainer = pl.Trainer(accelerator="auto", devices="auto")
    results = trainer.test(model, datamodule=datamodule)

    logger.info(f"Evaluation results: {results}")
    return results[0] if results else {}


def predict(model_path: str, image: torch.Tensor) -> torch.Tensor:
    """Run inference on a single image.

    Args:
        model_path: Path to model checkpoint
        image: Preprocessed image tensor [C, H, W]

    Returns:
        Class probabilities
    """
    model = SimpleCNN.load_from_checkpoint(model_path)
    model.eval()

    with torch.no_grad():
        if image.dim() == 3:
            image = image.unsqueeze(0)
        logits = model(image)
        probs = torch.softmax(logits, dim=1)
    return probs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True, help="Path to model checkpoint")
    parser.add_argument("--data-dir", default="data", help="Path to data directory")
    args = parser.parse_args()

    evaluate_model(args.checkpoint, args.data_dir)
