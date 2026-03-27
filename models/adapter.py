"""
Abstract model adapter interface
"""
from abc import ABC, abstractmethod


class ModelAdapter(ABC):
    """
    Abstract base class for AI model adapters
    Implements adapter pattern for model abstraction
    """
    
    @abstractmethod
    async def generate(self, prompt: str, model: str) -> str:
        """
        Generate response from AI model
        
        Args:
            prompt: Input prompt/query
            model: Model identifier
            
        Returns:
            Generated response text
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """
        Check if model service is available
        
        Returns:
            True if available, False otherwise
        """
        pass
