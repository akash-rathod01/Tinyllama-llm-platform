"""
Model Manager for Custom LLM Platform
Handles model loading, caching, and inference
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from typing import Optional, Dict, Any, Iterator
from threading import Thread
from loguru import logger
from config import Config

class ModelManager:
    """Manages model loading and inference"""
    
    def __init__(self, model_name: Optional[str] = None, quantized: Optional[bool] = None):
        self.model_name = model_name or Config.MODEL_NAME
        self.quantized = quantized if quantized is not None else Config.QUANTIZED
        self.model = None
        self.tokenizer = None
        self.device = Config.DEVICE
        
        logger.info(f"Initializing ModelManager for {self.model_name}")
        self._load_model()
    
    def _load_model(self):
        """Load model and tokenizer"""
        try:
            logger.info(f"Loading tokenizer for {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=Config.MODEL_CACHE_DIR if Config.USE_CACHE else None
            )
            
            # Set pad token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info(f"Loading model {self.model_name} (quantized={self.quantized})")
            
            if self.quantized:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    load_in_8bit=True,
                    device_map=self.device,
                    cache_dir=Config.MODEL_CACHE_DIR if Config.USE_CACHE else None
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    cache_dir=Config.MODEL_CACHE_DIR if Config.USE_CACHE else None
                )
                if self.device != "auto":
                    self.model.to(self.device)
            
            self.model.eval()
            logger.success(f"Model loaded successfully!")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def generate(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        num_return_sequences: int = 1,
        **kwargs
    ) -> str:
        """Generate text from prompt"""
        try:
            # Use config defaults if not specified
            max_length = max_length or Config.MAX_LENGTH
            temperature = temperature or Config.TEMPERATURE
            top_p = top_p or Config.TOP_P
            top_k = top_k or Config.TOP_K
            repetition_penalty = repetition_penalty or Config.REPETITION_PENALTY
            
            logger.info(f"Generating response for prompt: {prompt[:50]}...")
            
            inputs = self.tokenizer(prompt, return_tensors="pt", padding=True)
            
            # Move inputs to same device as model
            if not self.quantized and self.device != "auto":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    repetition_penalty=repetition_penalty,
                    num_return_sequences=num_return_sequences,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    **kwargs
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            logger.success("Response generated successfully")
            return response
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise
    
    def generate_stream(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        **kwargs
    ) -> Iterator[str]:
        """Generate text with streaming"""
        try:
            max_length = max_length or Config.MAX_LENGTH
            temperature = temperature or Config.TEMPERATURE
            top_p = top_p or Config.TOP_P
            top_k = top_k or Config.TOP_K
            repetition_penalty = repetition_penalty or Config.REPETITION_PENALTY
            
            logger.info(f"Streaming generation for prompt: {prompt[:50]}...")
            
            inputs = self.tokenizer(prompt, return_tensors="pt", padding=True)
            
            if not self.quantized and self.device != "auto":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            streamer = TextIteratorStreamer(
                self.tokenizer,
                skip_prompt=True,
                skip_special_tokens=True
            )
            
            generation_kwargs = {
                **inputs,
                "max_length": max_length,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "repetition_penalty": repetition_penalty,
                "do_sample": True,
                "pad_token_id": self.tokenizer.pad_token_id,
                "eos_token_id": self.tokenizer.eos_token_id,
                "streamer": streamer,
                **kwargs
            }
            
            # Run generation in separate thread
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()
            
            # Yield tokens as they're generated
            for text in streamer:
                yield text
            
            thread.join()
            logger.success("Streaming generation completed")
            
        except Exception as e:
            logger.error(f"Streaming generation failed: {e}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_name": self.model_name,
            "quantized": self.quantized,
            "device": str(self.device),
            "vocab_size": self.tokenizer.vocab_size,
            "model_max_length": self.tokenizer.model_max_length,
        }
