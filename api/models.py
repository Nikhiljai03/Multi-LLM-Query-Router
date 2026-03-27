"""
API request/response models
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class QueryComplexity(str, Enum):
    """Query complexity levels"""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class QueryRequest(BaseModel):
    """Request model for query endpoint"""
    query: str = Field(..., min_length=1, max_length=5000, description="User query text")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the capital of France?"
            }
        }


class QueryResponse(BaseModel):
    """Response model for query endpoint"""
    query: str
    response: str
    model_used: str
    complexity: QueryComplexity
    latency_ms: float
    cached: bool
    cost_estimate: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the capital of France?",
                "response": "The capital of France is Paris.",
                "model_used": "llama2:7b",
                "complexity": "simple",
                "latency_ms": 245.5,
                "cached": False,
                "cost_estimate": 0.001
            }
        }


class MetricsResponse(BaseModel):
    """Response model for metrics endpoint"""
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    queries_by_complexity: dict
    queries_by_model: dict
