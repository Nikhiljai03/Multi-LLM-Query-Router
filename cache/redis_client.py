"""
Redis cache client
"""
import json
import redis.asyncio as redis
from typing import Optional, Any
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RedisClient:
    """
    Async Redis client for caching
    """
    
    def __init__(self):
        self.host = settings.redis_host
        self.port = settings.redis_port
        self.db = settings.redis_db
        self.ttl = settings.cache_ttl
        self.client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Establish Redis connection"""
        self.client = await redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )
        logger.info(f"Connected to Redis at {self.host}:{self.port}")
    
    async def close(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()
            logger.info("Redis connection closed")
    
    async def ping(self) -> bool:
        """Check Redis connection"""
        if not self.client:
            return False
        try:
            return await self.client.ping()
        except:
            return False
    
    async def get(self, key: str) -> Optional[dict]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if not self.client:
            return None
        
        try:
            value = await self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis GET error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (optional)
        """
        if not self.client:
            return
        
        try:
            ttl = ttl or self.ttl
            await self.client.setex(
                key,
                ttl,
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Redis SET error: {e}")
