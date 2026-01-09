# APIs & FastAPI Guide

Source: https://skaftenicki.github.io/dtu_mlops/s7_deployment/apis/

## HTTP Fundamentals

### Request Components
- **URL**: Server location
- **Method**: Desired action (GET, POST, PUT, DELETE)

### Common HTTP Methods

| Method | Purpose |
|--------|---------|
| GET | Retrieve data |
| POST | Submit data |
| PUT | Update data |
| DELETE | Remove data |

## Python Requests Library

```python
import requests

# GET request
response = requests.get('https://api.github.com')
print(response.status_code)  # 200
print(response.json())       # Parse JSON

# With query parameters
response = requests.get(
    'https://api.github.com/search/repositories',
    params={'q': 'pytorch'}
)

# POST request
response = requests.post(
    'https://httpbin.org/post',
    json={'key': 'value'}
)

# Download file
response = requests.get('https://example.com/image.png')
with open('image.png', 'wb') as f:
    f.write(response.content)
```

## FastAPI Framework

### Installation

```bash
pip install fastapi uvicorn[standard]
```

### Basic Application

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}
```

### Run Server

```bash
uvicorn main:app --reload --port 8000
```

### Automatic Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI: `http://localhost:8000/openapi.json`

## Request Parameters

### Path Parameters

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### Query Parameters

```python
@app.get("/items")
def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### Request Body

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    quantity: int = 1

@app.post("/items")
def create_item(item: Item):
    return item
```

### File Upload

```python
from fastapi import File, UploadFile

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

## ML Application Integration

### Model Loading with Lifespan

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global model
    model = torch.load("model.pt")
    model.eval()
    yield
    # Shutdown
    del model

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file)
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(tensor)
    return {"prediction": output.argmax().item()}
```

## Docker Containerization

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Best Practices

1. Always specify types for automatic validation
2. Use appropriate HTTP methods
3. Load models during startup using lifespan events
4. Return meaningful status codes
5. Containerize applications for deployment
6. Use async for I/O-bound operations
7. Document endpoints with docstrings
