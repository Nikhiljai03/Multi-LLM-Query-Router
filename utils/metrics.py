"""
Metrics collection utilities
"""
from prometheus_client import Counter, Histogram, Gauge
from typing import Dict

# Query metrics
query_counter = Counter(
    'queries_total',
    'Total number of queries processed',
    ['complexity', 'model', 'cached']
)

query_latency = Histogram(
    'query_latency_seconds',
    'Query processing latency',
    ['complexity', 'model']
)

cache_hit_counter = Counter(
    'cache_hits_total',
    'Total number of cache hits'
)

cache_miss_counter = Counter(
    'cache_misses_total',
    'Total number of cache misses'
)

model_error_counter = Counter(
    'model_errors_total',
    'Total number of model errors',
    ['model']
)

active_requests = Gauge(
    'active_requests',
    'Number of requests currently being processed'
)


class MetricsCollector:
    """Centralized metrics collection"""
    
    @staticmethod
    def record_query(
        complexity: str,
        model: str,
        latency: float,
        cached: bool
    ):
        """Record query metrics"""
        query_counter.labels(
            complexity=complexity,
            model=model,
            cached=str(cached)
        ).inc()
        
        if not cached:
            query_latency.labels(
                complexity=complexity,
                model=model
            ).observe(latency)
    
    @staticmethod
    def record_cache_hit():
        """Record cache hit"""
        cache_hit_counter.inc()
    
    @staticmethod
    def record_cache_miss():
        """Record cache miss"""
        cache_miss_counter.inc()
    
    @staticmethod
    def record_model_error(model: str):
        """Record model error"""
        model_error_counter.labels(model=model).inc()
