"""
Groq model adapter - FREE and super fast!
Get API key from: https://console.groq.com/
"""
import httpx
from models.adapter import ModelAdapter
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class GroqAdapter(ModelAdapter):
    """
    Adapter for Groq API - FREE and extremely fast (1-2 second responses)
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'groq_api_key', None)
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.timeout = 30.0
        
        # Groq models from environment configuration
        self.model_map = {
            "simple": settings.groq_simple_model,
            "medium": settings.groq_medium_model,
            "complex": settings.groq_complex_model
        }
    
    async def generate(self, prompt: str, model: str) -> str:
        """
        Generate response using Groq API
        
        Args:
            prompt: Input prompt
            model: Model complexity (simple/medium/complex)
            
        Returns:
            Generated response text
        """
        if not self.api_key:
            raise Exception("Groq API key not configured. Get one free at https://console.groq.com/")
        
        # Map complexity to actual model
        actual_model = self.model_map.get(model, "llama3-8b-8192")
        
        logger.info(f"Calling Groq with model: {actual_model}")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": actual_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
            except httpx.HTTPError as e:
                logger.error(f"Groq API error: {e}")
                raise Exception(f"Groq request failed: {str(e)}")
    
    async def is_available(self) -> bool:
        """Check if Groq API is available"""
        return self.api_key is not None
