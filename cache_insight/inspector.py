# CacheInsight - Redis Inspector
import redis
from typing import Any, Dict
from .monitor import CacheMonitor

class CacheInspector:
    def __init__(self, redis_client: redis.Redis, monitor: CacheMonitor):
        self.redis_client = redis_client
        self.monitor = monitor
        
    def get_cached_value(self, key: str) -> Any:
        """Get value from cache and track hit/miss"""
        try:
            value = self.redis_client.get(key)
            if value is not None:
                self.monitor.record_cache_hit()
            else:
                self.monitor.record_cache_miss()
            return value
        except Exception as e:
            self.monitor.record_cache_miss()  # Treat errors as misses
            raise e
            
    def set_cached_value(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache and track operation"""
        try:
            result = self.redis_client.setex(key, ttl, value)
            self.monitor.track_operation('SET')
            return result
        except Exception as e:
            raise e
            
    def validate_data_integrity(self, key: str, expected_value: Any) -> Dict[str, Any]:
        """Validate that cached value matches expected value"""
        cached_value = self.get_cached_value(key)
        
        is_valid = cached_value == expected_value
        return {
            'key': key,
            'expected': expected_value,
            'cached': cached_value,
            'is_valid': is_valid,
            'match': is_valid
        }