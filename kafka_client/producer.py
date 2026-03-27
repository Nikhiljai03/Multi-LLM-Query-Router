"""
Kafka event producer
"""
import json
from kafka import KafkaProducer
from typing import Dict, Any, Optional
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class KafkaProducerClient:
    """
    Kafka producer for event logging (optional, non-blocking)
    """
    
    def __init__(self):
        self.bootstrap_servers = settings.kafka_bootstrap_servers.split(',')
        self.topic = settings.kafka_topic
        self.producer: Optional[KafkaProducer] = None
        self.initialization_failed = False
        
        # Don't initialize on startup - lazy load on first use
        logger.info("Kafka producer client created (lazy initialization)")
    
    def _initialize_producer(self):
        """Initialize Kafka producer with timeout (lazy loading)"""
        if self.producer or self.initialization_failed:
            return
        
        try:
            logger.info("Initializing Kafka producer...")
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks=0,  # Fire and forget (no acknowledgment)
                retries=0,  # Don't retry
                max_block_ms=1000,  # Only wait 1 second max
                request_timeout_ms=1000,  # 1 second timeout
                api_version_auto_timeout_ms=1000  # 1 second for version detection
            )
            logger.info(f"Kafka producer initialized: {self.bootstrap_servers}")
        except Exception as e:
            logger.warning(f"Kafka not available (will skip events): {e}")
            self.initialization_failed = True
    
    def send_event(self, event_data: Dict[str, Any]):
        """
        Send event to Kafka topic (non-blocking, fire-and-forget)
        
        Args:
            event_data: Event data dictionary
        """
        # Skip if initialization already failed
        if self.initialization_failed:
            return
        
        # Lazy initialize on first use
        if not self.producer:
            self._initialize_producer()
        
        # Skip if initialization failed
        if not self.producer:
            return
        
        try:
            # Send without waiting (fire and forget)
            self.producer.send(self.topic, event_data)
            logger.debug(f"Event queued for Kafka topic: {self.topic}")
        except Exception as e:
            # Just log, don't block
            logger.debug(f"Failed to queue Kafka event: {e}")
    
    def close(self):
        """Close Kafka producer"""
        if self.producer:
            try:
                self.producer.flush(timeout=1)  # Only wait 1 second
                self.producer.close(timeout=1)
                logger.info("Kafka producer closed")
            except Exception as e:
                logger.debug(f"Error closing Kafka producer: {e}")
