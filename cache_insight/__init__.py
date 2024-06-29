"""
Cache Insight - Redis-based testing tool

Provides monitoring and validation capabilities for Redis caching layers during testing.
"""

from .inspector import CacheInspector
from .monitor import RedisMonitor
from .analyzer import MetricsAnalyzer

__version__ = "0.1.0"
__author__ = "Cache Insight Team"

__all__ = [
    "CacheInspector",
    "RedisMonitor",
    "MetricsAnalyzer"
]