"""FastAPI application for model serving."""
{% if cookiecutter.use_fastapi == "yes" %}
from pathlib import Path

import torch
from fastapi import FastAPI, File, UploadFile
from loguru import logger
from PIL import Image
from torchvision import transforms

from {{ cookiecutter.project_slug }}.model import SimpleCNN

app = FastAPI(
    title="{{ cookiecutter.project_name }} API",
    description="Model inference API",
    version="0.1.0",
)

MODEL_PATH = Path("models/model.ckpt")
model = None
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


@app.on_event("startup")
async def load_model():
    """Load model on startup."""
    global model
    if MODEL_PATH.exists():
        model = SimpleCNN.load_from_checkpoint(str(MODEL_PATH))
        model.eval()
        logger.info(f"Model loaded from {MODEL_PATH}")
    else:
        logger.warning(f"No model found at {MODEL_PATH}. Serving without model.")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Run prediction on an uploaded image."""
    if model is None:
        return {"error": "No model loaded"}

    image = Image.open(file.file).convert("RGB")
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)
        predicted_class = torch.argmax(probs, dim=1).item()
        confidence = probs[0][predicted_class].item()

    return {
        "predicted_class": predicted_class,
        "confidence": round(confidence, 4),
        "probabilities": probs[0].tolist(),
    }
{% else %}
# FastAPI not enabled. Enable it by setting use_fastapi=yes during project creation.
{% endif %}
