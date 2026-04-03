"""
Example usage of the Custom LLM API
"""
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())

def test_model_info():
    """Get model information"""
    response = requests.get(f"{BASE_URL}/model/info")
    print("\nModel Info:", json.dumps(response.json(), indent=2))

def test_generate():
    """Test text generation"""
    payload = {
        "prompt": "Once upon a time in a distant galaxy,",
        "max_length": 100,
        "temperature": 0.7,
        "stream": False
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    result = response.json()
    
    print("\n=== Generation Test ===")
    print(f"Prompt: {result['prompt']}")
    print(f"Generated: {result['generated_text']}")
    print(f"Tokens: {result['tokens_used']}")

def test_chat():
    """Test chat endpoint"""
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "What is machine learning?"}
        ],
        "max_length": 150,
        "temperature": 0.7,
        "stream": False
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    result = response.json()
    
    print("\n=== Chat Test ===")
    print(f"Response: {result['response']}")

def test_streaming():
    """Test streaming generation"""
    payload = {
        "prompt": "Write a haiku about coding:",
        "max_length": 50,
        "temperature": 0.8
    }
    
    print("\n=== Streaming Test ===")
    print("Prompt:", payload['prompt'])
    print("Response: ", end="")
    
    response = requests.post(
        f"{BASE_URL}/generate/stream",
        json=payload,
        stream=True
    )
    
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk:
            print(chunk, end="", flush=True)
    print()

if __name__ == "__main__":
    print("Testing Custom LLM API...\n")
    
    try:
        test_health()
        test_model_info()
        test_generate()
        test_chat()
        test_streaming()
        
        print("\n✓ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        print("Make sure the server is running: python api_server.py")
    except Exception as e:
        print(f"Error: {e}")
