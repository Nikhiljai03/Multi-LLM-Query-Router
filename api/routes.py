"""
API route handlers
"""
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
import time
import hashlib

from api.models import QueryRequest, QueryResponse, MetricsResponse
from router.classifier import QueryClassifier
from router.query_router import QueryRouter
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

# Initialize components
classifier = QueryClassifier()
query_router = QueryRouter()


@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: Request,
    query_request: QueryRequest
):
    """
    Main query processing endpoint
    
    Flow:
    1. Check cache
    2. Classify query complexity
    3. Route to appropriate model
    4. Cache response
    5. Log event to Kafka
    """
    start_time = time.time()
    query_text = query_request.query
    
    logger.info(f"Processing query: {query_text[:50]}...")
    
    # Generate cache key
    cache_key = f"query:{hashlib.md5(query_text.encode()).hexdigest()}"
    
    # Check cache
    redis_client = request.app.state.redis
    cached_response = None
    
    if redis_client:
        try:
            cached_response = await redis_client.get(cache_key)
            if cached_response:
                logger.info("Cache hit - returning cached response")
                cached_response["cached"] = True
                cached_response["latency_ms"] = (time.time() - start_time) * 1000
                return cached_response
        except Exception as e:
            logger.warning(f"Cache check failed: {e}")
    
    # Classify query complexity
    complexity = classifier.classify(query_text)
    logger.info(f"Query classified as: {complexity}")
    
    # Route query to appropriate model
    try:
        response_text, model_used, cost = await query_router.route_query(
            query_text, 
            complexity
        )
    except Exception as e:
        logger.error(f"Query routing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")
    
    # Calculate latency
    latency_ms = (time.time() - start_time) * 1000
    
    # Prepare response
    response_data = {
        "query": query_text,
        "response": response_text,
        "model_used": model_used,
        "complexity": complexity,
        "latency_ms": round(latency_ms, 2),
        "cached": False,
        "cost_estimate": cost
    }
    
    # Send event to Kafka (fire and forget, don't wait at all)
    kafka_client = request.app.state.kafka
    if kafka_client:
        # Run in background, don't wait
        import asyncio
        asyncio.create_task(asyncio.to_thread(kafka_client.send_event, {
            **response_data,
            "timestamp": time.time()
        }))
    
    # Cache response (async, don't wait)
    if redis_client:
        try:
            await redis_client.set(cache_key, response_data)
            logger.info("Response cached successfully")
        except Exception as e:
            logger.warning(f"Failed to cache response (non-blocking): {e}")
    
    return response_data


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(request: Request):
    """
    Get basic system metrics
    """
    # This is a basic implementation
    # In production, you'd aggregate from database or metrics store
    return {
        "total_queries": 0,
        "cache_hit_rate": 0.0,
        "avg_latency_ms": 0.0,
        "queries_by_complexity": {
            "simple": 0,
            "medium": 0,
            "complex": 0
        },
        "queries_by_model": {}
    }
