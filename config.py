"""
Configuration management for Custom LLM Platform
"""
import os
import json
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Central configuration class"""
    
    # Model Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "EleutherAI/gpt-j-6B")
    QUANTIZED: bool = os.getenv("QUANTIZED", "true").lower() == "true"
    DEVICE: str = os.getenv("DEVICE", "auto")
    
    # Generation Parameters
    MAX_LENGTH: int = int(os.getenv("MAX_LENGTH", "512"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P: float = float(os.getenv("TOP_P", "0.9"))
    TOP_K: int = int(os.getenv("TOP_K", "50"))
    REPETITION_PENALTY: float = float(os.getenv("REPETITION_PENALTY", "1.1"))
    
    # API Server
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_RELOAD: bool = os.getenv("API_RELOAD", "false").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # Model Cache
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", "./model_cache")
    USE_CACHE: bool = os.getenv("USE_CACHE", "true").lower() == "true"
    
    # Training
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "1"))
    LEARNING_RATE: float = float(os.getenv("LEARNING_RATE", "5e-5"))
    NUM_EPOCHS: int = int(os.getenv("NUM_EPOCHS", "3"))
    GRADIENT_ACCUMULATION_STEPS: int = int(os.getenv("GRADIENT_ACCUMULATION_STEPS", "4"))
    SAVE_STEPS: int = int(os.getenv("SAVE_STEPS", "100"))
    
    # Advanced Features
    ENABLE_STREAMING: bool = os.getenv("ENABLE_STREAMING", "true").lower() == "true"
    MAX_CONVERSATION_HISTORY: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))
    ENABLE_CONTEXT_MEMORY: bool = os.getenv("ENABLE_CONTEXT_MEMORY", "true").lower() == "true"
    
    @classmethod
    def load_from_json(cls, config_path: str = "config.json") -> dict:
        """Load additional config from JSON file"""
        if Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    @classmethod
    def get_model_config(cls) -> dict:
        """Get model-specific configuration"""
        return {
            "model_name": cls.MODEL_NAME,
            "quantized": cls.QUANTIZED,
            "device": cls.DEVICE,
            "cache_dir": cls.MODEL_CACHE_DIR if cls.USE_CACHE else None,
        }
    
    @classmethod
    def get_generation_config(cls) -> dict:
        """Get generation parameters"""
        return {
            "max_length": cls.MAX_LENGTH,
            "temperature": cls.TEMPERATURE,
            "top_p": cls.TOP_P,
            "top_k": cls.TOP_K,
            "repetition_penalty": cls.REPETITION_PENALTY,
        }

# Create necessary directories
Path(Config.MODEL_CACHE_DIR).mkdir(parents=True, exist_ok=True)
Path(Config.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
