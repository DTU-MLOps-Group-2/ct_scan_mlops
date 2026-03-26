"""Data loading and preprocessing."""

from pathlib import Path

import pytorch_lightning as pl
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision import transforms


class ImageDataset(Dataset):
    """Generic image dataset.

    Expects directory structure:
        data_dir/
            class_a/
                img1.png
                img2.png
            class_b/
                img3.png
                ...
    """

    def __init__(self, data_dir: str | Path, transform=None):
        from PIL import Image

        self.data_dir = Path(data_dir)
        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        self.classes = sorted([d.name for d in self.data_dir.iterdir() if d.is_dir()])
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}

        self.samples = []
        for cls_dir in self.data_dir.iterdir():
            if cls_dir.is_dir():
                label = self.class_to_idx[cls_dir.name]
                for img_path in cls_dir.glob("*"):
                    if img_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}:
                        self.samples.append((img_path, label))

        self._Image = Image

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int):
        img_path, label = self.samples[idx]
        image = self._Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label


class DataModule(pl.LightningDataModule):
    """Lightning DataModule for image classification."""

    def __init__(
        self,
        data_dir: str = "data",
        batch_size: int = 32,
        num_workers: int = 4,
        val_split: float = 0.2,
        test_split: float = 0.1,
        image_size: int = 224,
    ):
        super().__init__()
        self.save_hyperparameters()
        self.data_dir = Path(data_dir)
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.val_split = val_split
        self.test_split = test_split

        self.transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def setup(self, stage=None):
        full_dataset = ImageDataset(self.data_dir, transform=self.transform)

        total = len(full_dataset)
        test_size = int(total * self.test_split)
        val_size = int(total * self.val_split)
        train_size = total - val_size - test_size

        self.train_dataset, self.val_dataset, self.test_dataset = random_split(
            full_dataset, [train_size, val_size, test_size]
        )

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            pin_memory=True,
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            pin_memory=True,
        )
