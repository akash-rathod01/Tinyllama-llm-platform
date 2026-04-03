"""
FastAPI Server for Custom LLM Platform
Provides REST API endpoints for model inference
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uvicorn
from loguru import logger
import sys

from model_manager import ModelManager
from config import Config

# Configure logging
logger.remove()
logger.add(sys.stderr, level=Config.LOG_LEVEL)
logger.add(Config.LOG_FILE, rotation="500 MB", level=Config.LOG_LEVEL)

# Initialize FastAPI app
app = FastAPI(
    title="Custom LLM API",
    description="REST API for custom LLM inference",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model manager
model_manager: Optional[ModelManager] = None

# Request/Response Models
class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Input prompt for generation")
    max_length: Optional[int] = Field(None, description="Maximum length of generated text")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    top_k: Optional[int] = Field(None, ge=0, description="Top-k sampling parameter")
    repetition_penalty: Optional[float] = Field(None, ge=1.0, description="Repetition penalty")
    stream: bool = Field(False, description="Enable streaming response")

class GenerateResponse(BaseModel):
    generated_text: str
    prompt: str
    tokens_used: int
    model: str
    timestamp: str

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="Conversation history")
    max_length: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    stream: bool = False

class ModelInfo(BaseModel):
    model_name: str
    quantized: bool
    device: str
    vocab_size: int
    model_max_length: int
    config: Dict[str, Any]

# Conversation history storage (in-memory, for demo)
conversations: Dict[str, List[ChatMessage]] = {}

@app.on_event("startup")
async def startup_event():
    """Initialize model on startup"""
    global model_manager
    try:
        logger.info("Starting Custom LLM API Server...")
        model_manager = ModelManager()
        logger.success("Model loaded and ready!")
    except Exception as e:
        logger.error(f"Failed to initialize model: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint"""
    return {
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model_manager is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get model information"""
    if model_manager is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    info = model_manager.get_model_info()
    return ModelInfo(
        **info,
        config=Config.get_generation_config()
    )

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text from prompt"""
    if model_manager is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        logger.info(f"Received generation request: {request.prompt[:50]}...")
        
        if request.stream:
            raise HTTPException(
                status_code=400,
                detail="Use /generate/stream endpoint for streaming responses"
            )
        
        generated_text = model_manager.generate(
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            repetition_penalty=request.repetition_penalty
        )
        
        tokens_used = model_manager.count_tokens(generated_text)
        
        return GenerateResponse(
            generated_text=generated_text,
            prompt=request.prompt,
            tokens_used=tokens_used,
            model=model_manager.model_name,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/stream")
async def generate_text_stream(request: GenerateRequest):
    """Generate text with streaming"""
    if model_manager is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not Config.ENABLE_STREAMING:
        raise HTTPException(status_code=400, detail="Streaming is disabled")
    
    try:
        logger.info(f"Received streaming generation request: {request.prompt[:50]}...")
        
        def generate():
            for text_chunk in model_manager.generate_stream(
                prompt=request.prompt,
                max_length=request.max_length,
                temperature=request.temperature,
                top_p=request.top_p,
                top_k=request.top_k,
                repetition_penalty=request.repetition_penalty
            ):
                yield text_chunk
        
        return StreamingResponse(generate(), media_type="text/plain")
        
    except Exception as e:
        logger.error(f"Streaming generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint with conversation context"""
    if model_manager is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Build prompt from conversation history
        prompt = ""
        for msg in request.messages:
            if msg.role == "system":
                prompt += f"System: {msg.content}\n\n"
            elif msg.role == "user":
                prompt += f"User: {msg.content}\n\n"
            elif msg.role == "assistant":
                prompt += f"Assistant: {msg.content}\n\n"
        
        prompt += "Assistant:"
        
        logger.info(f"Chat request with {len(request.messages)} messages")
        
        if request.stream:
            def generate():
                for text_chunk in model_manager.generate_stream(
                    prompt=prompt,
                    max_length=request.max_length,
                    temperature=request.temperature,
                    top_p=request.top_p
                ):
                    yield text_chunk
            
            return StreamingResponse(generate(), media_type="text/plain")
        else:
            response = model_manager.generate(
                prompt=prompt,
                max_length=request.max_length,
                temperature=request.temperature,
                top_p=request.top_p
            )
            
            # Extract only the assistant's response
            assistant_response = response.split("Assistant:")[-1].strip()
            
            return {
                "response": assistant_response,
                "model": model_manager.model_name,
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info(f"Starting server on {Config.API_HOST}:{Config.API_PORT}")
    uvicorn.run(
        "api_server:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.API_RELOAD
    )
