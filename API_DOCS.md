# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Root
**GET /**

Get API information and available endpoints.

**Response:**
```json
{
  "message": "Custom LLM API Server",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "generate": "/generate",
    "chat": "/chat",
    "model_info": "/model/info",
    "health": "/health"
  }
}
```

---

### 2. Health Check
**GET /health**

Check if the API is running and model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-01T12:00:00"
}
```

---

### 3. Model Information
**GET /model/info**

Get information about the loaded model.

**Response:**
```json
{
  "model_name": "EleutherAI/gpt-j-6B",
  "quantized": true,
  "device": "cuda:0",
  "vocab_size": 50400,
  "model_max_length": 2048,
  "config": {
    "max_length": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "repetition_penalty": 1.1
  }
}
```

---

### 4. Generate Text
**POST /generate**

Generate text from a prompt.

**Request Body:**
```json
{
  "prompt": "Once upon a time",
  "max_length": 100,
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 50,
  "repetition_penalty": 1.1,
  "stream": false
}
```

**Parameters:**
- `prompt` (required): Input text prompt
- `max_length` (optional): Maximum length of generated text (default: 512)
- `temperature` (optional): Sampling temperature 0.0-2.0 (default: 0.7)
- `top_p` (optional): Nucleus sampling parameter 0.0-1.0 (default: 0.9)
- `top_k` (optional): Top-k sampling parameter (default: 50)
- `repetition_penalty` (optional): Penalty for repetition ≥1.0 (default: 1.1)
- `stream` (optional): Must be false for this endpoint

**Response:**
```json
{
  "generated_text": "Once upon a time in a distant galaxy...",
  "prompt": "Once upon a time",
  "tokens_used": 87,
  "model": "EleutherAI/gpt-j-6B",
  "timestamp": "2024-01-01T12:00:00"
}
```

---

### 5. Generate Text (Streaming)
**POST /generate/stream**

Generate text with streaming response.

**Request Body:**
```json
{
  "prompt": "Write a haiku about coding",
  "max_length": 50,
  "temperature": 0.8,
  "top_p": 0.9,
  "top_k": 50,
  "repetition_penalty": 1.1
}
```

**Response:**
Streaming text/plain response with tokens generated in real-time.

**Example (Python):**
```python
import requests

response = requests.post(
    "http://localhost:8000/generate/stream",
    json={"prompt": "Write a story"},
    stream=True
)

for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
    if chunk:
        print(chunk, end="", flush=True)
```

---

### 6. Chat
**POST /chat**

Chat with conversation context.

**Request Body:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful AI assistant."
    },
    {
      "role": "user",
      "content": "What is machine learning?"
    }
  ],
  "max_length": 150,
  "temperature": 0.7,
  "top_p": 0.9,
  "stream": false
}
```

**Message Roles:**
- `system`: System instructions/context
- `user`: User messages
- `assistant`: Previous assistant responses

**Response (Non-streaming):**
```json
{
  "response": "Machine learning is a subset of artificial intelligence...",
  "model": "EleutherAI/gpt-j-6B",
  "timestamp": "2024-01-01T12:00:00"
}
```

**Response (Streaming):**
Streaming text/plain response when `stream: true`

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid parameter value"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Generation failed: <error message>"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Model not loaded"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider adding rate limiting middleware.

---

## Authentication

Currently no authentication is required. For production use, implement API key or OAuth authentication.

---

## Examples

### cURL Examples

**Generate Text:**
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The future of AI is",
    "max_length": 100,
    "temperature": 0.7
  }'
```

**Chat:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### Python Examples

**Using requests:**
```python
import requests

# Generate
response = requests.post(
    "http://localhost:8000/generate",
    json={
        "prompt": "Once upon a time",
        "max_length": 100
    }
)
print(response.json()["generated_text"])

# Chat
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "messages": [
            {"role": "user", "content": "What is Python?"}
        ]
    }
)
print(response.json()["response"])
```

### JavaScript Examples

**Using fetch:**
```javascript
// Generate
fetch('http://localhost:8000/generate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    prompt: 'The future of technology',
    max_length: 100
  })
})
.then(r => r.json())
.then(data => console.log(data.generated_text));

// Chat
fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    messages: [
      {role: 'user', content: 'Hello!'}
    ]
  })
})
.then(r => r.json())
.then(data => console.log(data.response));
```
