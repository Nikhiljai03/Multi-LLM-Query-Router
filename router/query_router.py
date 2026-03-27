"""
Query router - routes queries to appropriate models
"""
from typing import Tuple
from models.groq_adapter import GroqAdapter
from models.together_adapter import TogetherAdapter
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class QueryRouter:
    """
    Routes queries to appropriate AI models based on complexity
    Implements fallback mechanism for reliability
    """
    
    def __init__(self):
        # Initialize Groq as primary adapter
        logger.info("Using GROQ adapter (FREE, super fast cloud API)")
        self.primary_adapter = GroqAdapter()
        
        # Setup fallback to Together AI if configured
        use_together = getattr(settings, 'use_together_as_fallback', False)
        together_key = getattr(settings, 'together_api_key', None)
        
        if use_together and together_key:
            logger.info("Together AI configured as fallback")
            self.fallback_adapter = TogetherAdapter()
        else:
            logger.info("No fallback adapter configured")
            self.fallback_adapter = None
        
        # Fallback configuration
        self.enable_fallback = settings.enable_fallback
        
        # Cost estimates per complexity tier
        self.cost_map = {
            "simple": 0.001,   # Smallest models
            "medium": 0.005,   # Medium models
            "complex": 0.02    # Largest models
        }
    
    async def route_query(
        self, 
        query: str, 
        complexity: str
    ) -> Tuple[str, str, float]:
        """
        Route query to appropriate model with fallback
        
        Args:
            query: User query text
            complexity: Query complexity level (simple/medium/complex)
            
        Returns:
            Tuple of (response_text, model_used, cost)
        """
        logger.info(f"Routing {complexity} query to primary adapter")
        
        try:
            # Try primary adapter (Groq or Ollama)
            response = await self.primary_adapter.generate(query, complexity)
            
            # Get the actual model name used
            model_name = self.primary_adapter.model_map.get(complexity, "unknown")
            cost = self.cost_map.get(complexity, 0.01)
            
            logger.info(f"Primary adapter succeeded with model: {model_name}")
            return response, model_name, cost
            
        except Exception as e:
            logger.error(f"Primary adapter failed: {e}")
            
            # Check if fallback is enabled and available
            if not self.enable_fallback or not self.fallback_adapter:
                logger.error("No fallback available. Returning error.")
                return (
                    "I apologize, but I'm currently unable to process your request. Please try again later.",
                    "error_no_fallback",
                    0.0
                )
            
            # Try fallback adapter (Together AI)
            logger.info(f"Attempting fallback to Together AI for {complexity} query")
            
            try:
                response = await self.fallback_adapter.generate(query, complexity)
                
                # Get the actual fallback model name
                fallback_model = self.fallback_adapter.model_map.get(complexity, "unknown")
                cost = self.cost_map.get(complexity, 0.01)
                
                logger.info(f"Fallback succeeded with model: {fallback_model}")
                return response, f"{fallback_model} (fallback)", cost
                
            except Exception as fallback_error:
                logger.error(f"Fallback adapter also failed: {fallback_error}")
                
                # Last resort: return error message
                return (
                    "I apologize, but I'm currently unable to process your request. Please try again later.",
                    "error_all_models_failed",
                    0.0
                )
