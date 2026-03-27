"""
AI Query Router - Main Application Entry Point
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
import os

from config.settings import settings
from utils.logger import setup_logger
from api.routes import router as api_router
from cache.redis_client import RedisClient
from kafka_client.producer import KafkaProducerClient

# Setup logger
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager - handles startup and shutdown
    """
    # Startup
    logger.info("Starting AI Query Router...")
    
    # Initialize Redis
    try:
        redis_client = RedisClient()
        await redis_client.connect()
        app.state.redis = redis_client
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        app.state.redis = None
    
    # Initialize Kafka
    try:
        kafka_client = KafkaProducerClient()
        app.state.kafka = kafka_client
        logger.info("Kafka producer initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Kafka: {e}")
        app.state.kafka = None
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Query Router...")
    
    if app.state.redis:
        await app.state.redis.close()
        logger.info("Redis connection closed")
    
    if app.state.kafka:
        app.state.kafka.close()
        logger.info("Kafka producer closed")
    
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-level AI Query Router with multi-model LLM support",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add request processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Serve the main UI"""
    return FileResponse('static/index.html')


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    health_status = {
        "status": "healthy",
        "redis": "unknown",
        "kafka": "unknown"
    }
    
    # Check Redis
    if app.state.redis:
        try:
            await app.state.redis.ping()
            health_status["redis"] = "connected"
        except:
            health_status["redis"] = "disconnected"
            health_status["status"] = "degraded"
    
    # Check Kafka
    if app.state.kafka:
        health_status["kafka"] = "initialized"
    
    return health_status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=False  # Disabled auto-reload to prevent constant restarts
    )
