"""
Together AI adapter - FREE with generous limits
Get API key from: https://api.together.xyz/
"""
import httpx
from models.adapter import ModelAdapter
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TogetherAdapter(ModelAdapter):
    """
    Adapter for Together AI - FREE and fast (great as fallback)
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'together_api_key', None)
        self.base_url = "https://api.together.xyz/v1/chat/completions"
        self.timeout = 30.0
        
        # Together AI models from environment configuration
        self.model_map = {
            "simple": settings.together_simple_model,
            "medium": settings.together_medium_model,
            "complex": settings.together_complex_model
        }
    
    async def generate(self, prompt: str, model: str) -> str:
        """
        Generate response using Together AI API
        
        Args:
            prompt: Input prompt
            model: Model complexity (simple/medium/complex)
            
        Returns:
            Generated response text
        """
        if not self.api_key:
            raise Exception("Together AI API key not configured. Get one free at https://api.together.xyz/")
        
        # Map complexity to actual model
        actual_model = self.model_map.get(model, "meta-llama/Llama-3-8b-chat-hf")
        
        logger.info(f"Calling Together AI with model: {actual_model}")
        
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
                logger.error(f"Together AI API error: {e}")
                raise Exception(f"Together AI request failed: {str(e)}")
    
    async def is_available(self) -> bool:
        """Check if Together AI API is available"""
        return self.api_key is not None
