# Frontend Development Guide

Source: https://skaftenicki.github.io/dtu_mlops/s7_deployment/frontend/

## Framework Overview

**Streamlit** is recommended for ML application frontends—easy to get started and integrates well with ML models.

Other options: Django, Reflex, Bokeh, Gradio

## Architecture Pattern

Separate frontend and backend for independent scaling:

```
┌──────────────┐     ┌──────────────┐
│   Frontend   │────▶│   Backend    │
│  (Streamlit) │     │  (FastAPI)   │
└──────────────┘     └──────────────┘
       │                    │
       ▼                    ▼
    Users              ML Model
```

## Streamlit Basics

### Installation

```bash
pip install streamlit
```

### Basic App

```python
import streamlit as st
import requests

st.title("ML Application")

# File upload
uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Display image
    st.image(uploaded_file, caption="Uploaded Image")

    # Predict button
    if st.button("Classify"):
        # Send to backend
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://backend:8000/predict", files=files)

        if response.ok:
            result = response.json()
            st.success(f"Prediction: {result['class']}")
            st.bar_chart(result['probabilities'])
```

### Run App

```bash
streamlit run app.py
```

## Key Streamlit Components

```python
import streamlit as st

# Text
st.title("Title")
st.header("Header")
st.subheader("Subheader")
st.text("Plain text")
st.markdown("**Markdown** support")

# Input widgets
text = st.text_input("Enter text")
number = st.number_input("Enter number", min_value=0, max_value=100)
option = st.selectbox("Choose option", ["A", "B", "C"])
slider = st.slider("Select value", 0, 100, 50)

# Display
st.image(image)
st.dataframe(df)
st.pyplot(fig)
st.json(data)

# Layout
col1, col2 = st.columns(2)
with col1:
    st.write("Column 1")
with col2:
    st.write("Column 2")

# Sidebar
st.sidebar.title("Settings")

# Caching
@st.cache_resource
def load_model():
    return torch.load("model.pt")
```

## Backend Integration

### FastAPI Backend

```python
from fastapi import FastAPI, File, UploadFile
import torch

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file)
    tensor = transform(image)

    with torch.no_grad():
        output = model(tensor.unsqueeze(0))

    probs = torch.softmax(output, dim=1)
    return {
        "class": classes[probs.argmax()],
        "probabilities": probs.tolist()
    }
```

### Streamlit Frontend

```python
import streamlit as st
import requests

@st.cache_resource
def get_backend_url():
    # Use service discovery or environment variable
    return os.getenv("BACKEND_URL", "http://localhost:8000")

def predict(image_bytes):
    url = f"{get_backend_url()}/predict"
    response = requests.post(url, files={"file": image_bytes})
    return response.json()
```

## Docker Deployment

### Frontend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements_frontend.txt .
RUN pip install --no-cache-dir -r requirements_frontend.txt

COPY app.py .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

### Docker Compose

```yaml
version: '3'
services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
```

## Best Practices

1. **Separate requirements files** for frontend and backend
2. **Use caching** (`@st.cache_resource`) for expensive operations
3. **Service discovery** for dynamic backend URLs in cloud
4. **Error handling** for backend communication failures
5. **Loading indicators** for long operations
6. **Responsive design** using columns and containers
