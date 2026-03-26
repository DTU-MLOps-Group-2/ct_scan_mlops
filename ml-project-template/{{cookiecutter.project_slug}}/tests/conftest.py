"""Pytest configuration and shared fixtures."""

import pytest
import torch


@pytest.fixture
def sample_image():
    """Create a random sample image tensor."""
    return torch.randn(1, 3, 224, 224)


@pytest.fixture
def sample_batch():
    """Create a random batch of images with labels."""
    images = torch.randn(4, 3, 224, 224)
    labels = torch.randint(0, 10, (4,))
    return images, labels


@pytest.fixture
def device():
    """Get the best available device for testing."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")
