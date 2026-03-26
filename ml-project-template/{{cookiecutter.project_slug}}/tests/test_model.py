"""Tests for model definitions."""

import torch

from {{ cookiecutter.project_slug }}.model import BaseModel, SimpleCNN


class TestBaseModel:
    def test_forward_pass(self, sample_batch):
        model = BaseModel(num_classes=10)
        images, _ = sample_batch
        output = model(images)
        assert output.shape == (4, 10)

    def test_training_step(self, sample_batch):
        model = BaseModel(num_classes=10)
        loss = model.training_step(sample_batch, 0)
        assert loss is not None
        assert loss.dim() == 0  # scalar


class TestSimpleCNN:
    def test_forward_pass(self, sample_batch):
        model = SimpleCNN(num_classes=10, in_channels=3)
        images, _ = sample_batch
        output = model(images)
        assert output.shape == (4, 10)

    def test_output_probabilities(self, sample_image):
        model = SimpleCNN(num_classes=10)
        model.eval()
        with torch.no_grad():
            logits = model(sample_image)
            probs = torch.softmax(logits, dim=1)
        assert torch.allclose(probs.sum(dim=1), torch.tensor([1.0]), atol=1e-5)

    def test_configure_optimizers(self):
        model = SimpleCNN(num_classes=10, lr=0.01)
        optimizer = model.configure_optimizers()
        assert isinstance(optimizer, torch.optim.Adam)
