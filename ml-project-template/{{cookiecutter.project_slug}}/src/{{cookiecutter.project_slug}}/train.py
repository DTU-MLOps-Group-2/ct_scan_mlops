"""Training entrypoint."""
{% if cookiecutter.use_hydra == "yes" %}
import hydra
from omegaconf import DictConfig
{% endif %}
import pytorch_lightning as pl
from loguru import logger
{% if cookiecutter.use_wandb == "yes" %}
from pytorch_lightning.loggers import WandbLogger
{% endif %}

from {{ cookiecutter.project_slug }}.data import DataModule
from {{ cookiecutter.project_slug }}.model import SimpleCNN

{% if cookiecutter.use_hydra == "yes" %}

@hydra.main(config_path="../../configs", config_name="config", version_base="1.3")
def main(cfg: DictConfig) -> None:
    """Train the model using Hydra configuration."""
    logger.info(f"Training with config: {cfg}")

    # Data
    datamodule = DataModule(
        data_dir=cfg.data.data_dir,
        batch_size=cfg.train.batch_size,
        num_workers=cfg.data.num_workers,
        image_size=cfg.data.image_size,
    )

    # Model
    model = SimpleCNN(
        num_classes=cfg.model.num_classes,
        lr=cfg.train.lr,
        in_channels=cfg.model.in_channels,
    )

    # Logger
    {%- if cookiecutter.use_wandb == "yes" %}
    wandb_logger = WandbLogger(
        project=cfg.get("wandb", {}).get("project", "{{ cookiecutter.project_slug }}"),
        name=cfg.get("experiment_name", None),
    )
    trainer_logger = wandb_logger
    {%- else %}
    trainer_logger = True  # default TensorBoard logger
    {%- endif %}

    # Trainer
    trainer = pl.Trainer(
        max_epochs=cfg.train.max_epochs,
        accelerator="auto",
        devices="auto",
        logger=trainer_logger,
        callbacks=[
            pl.callbacks.ModelCheckpoint(
                monitor="val_acc",
                mode="max",
                save_top_k=1,
                dirpath=cfg.get("output_dir", "outputs/checkpoints"),
            ),
            pl.callbacks.EarlyStopping(
                monitor="val_loss",
                patience=cfg.train.get("patience", 10),
                mode="min",
            ),
        ],
    )

    trainer.fit(model, datamodule=datamodule)
    trainer.test(model, datamodule=datamodule)

{% else %}

def main() -> None:
    """Train the model."""
    logger.info("Starting training...")

    datamodule = DataModule(data_dir="data", batch_size=32, image_size=224)

    model = SimpleCNN(num_classes=10, lr=1e-3)

    {%- if cookiecutter.use_wandb == "yes" %}
    wandb_logger = WandbLogger(project="{{ cookiecutter.project_slug }}")
    trainer_logger = wandb_logger
    {%- else %}
    trainer_logger = True
    {%- endif %}

    trainer = pl.Trainer(
        max_epochs=50,
        accelerator="auto",
        devices="auto",
        logger=trainer_logger,
        callbacks=[
            pl.callbacks.ModelCheckpoint(monitor="val_acc", mode="max", save_top_k=1),
            pl.callbacks.EarlyStopping(monitor="val_loss", patience=10, mode="min"),
        ],
    )

    trainer.fit(model, datamodule=datamodule)
    trainer.test(model, datamodule=datamodule)

{% endif %}

if __name__ == "__main__":
    main()
