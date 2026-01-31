"""
LLM client for free, local models (Ollama or HuggingFace)
"""
from typing import Optional, Dict, Any
import json
import requests
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from src.utils.logger import logger

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    logger.warning("HuggingFace transformers not available. Install with: pip install transformers torch")

class LLMClient:
    """Client for interacting with free LLM models"""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = None
        self.tokenizer = None
        
        if self.provider == "ollama":
            self._init_ollama()
        elif self.provider == "huggingface":
            if not HF_AVAILABLE:
                raise ImportError("HuggingFace transformers required for HF provider")
            self._init_huggingface()
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")
    
    def _init_ollama(self):
        """Initialize Ollama client"""
        self.base_url = settings.OLLAMA_BASE_URL
        self.model_name = settings.OLLAMA_MODEL
        
        # Check if Ollama is running
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                logger.warning("Ollama may not be running. Start with: ollama serve")
        except Exception as e:
            logger.warning(f"Could not connect to Ollama: {e}")
    
    def _init_huggingface(self):
        """Initialize HuggingFace model"""
        logger.info(f"Loading HuggingFace model: {settings.HF_MODEL}")
        self.tokenizer = AutoTokenizer.from_pretrained(settings.HF_MODEL)
        self.model = AutoModelForCausalLM.from_pretrained(
            settings.HF_MODEL,
            device_map=settings.HF_DEVICE,
            torch_dtype=torch.float16 if settings.HF_DEVICE == "cuda" else torch.float32
        )
        logger.info("HuggingFace model loaded successfully")
    
    def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.1) -> str:
        """Generate text from prompt"""
        if self.provider == "ollama":
            return self._generate_ollama(prompt, max_tokens, temperature)
        elif self.provider == "huggingface":
            return self._generate_huggingface(prompt, max_tokens, temperature)
    
    def _generate_ollama(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature
                    }
                },
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except Exception as e:
            logger.error(f"Error generating with Ollama: {e}")
            raise
    
    def _generate_huggingface(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using HuggingFace"""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            if settings.HF_DEVICE == "cuda":
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove the prompt from the output
            return generated_text[len(prompt):].strip()
        except Exception as e:
            logger.error(f"Error generating with HuggingFace: {e}")
            raise
    
    def extract_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structured data using LLM with JSON schema"""
        json_schema = json.dumps(schema, indent=2)
        
        structured_prompt = f"""Extract information from the following text and return it as JSON matching this schema:

Schema:
{json_schema}

Text:
{prompt}

Return ONLY valid JSON, no additional text."""
        
        response = self.generate(structured_prompt, max_tokens=2000, temperature=0)
        
        # Try to extract JSON from response
        try:
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            logger.error(f"Error parsing JSON from LLM response: {e}")
            logger.debug(f"Response was: {response}")
            raise
