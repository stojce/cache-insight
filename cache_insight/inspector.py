import time
import redis
from typing import Dict, Any, Optional, ContextManager
from contextlib import contextmanager

from .monitor import RedisMonitor
from .analyzer import MetricsAnalyzer


class CacheInspector:
    """
    Main class for inspecting Redis cache behavior during tests.
    Tracks operations, analyzes performance, and validates data integrity.
    """
    
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.monitor = RedisMonitor(self.redis_client)
        self.analyzer = MetricsAnalyzer()
        
    def start_monitoring(self):
        """Start tracking Redis operations"""
        self.monitor.start_tracking()
        
    def stop_monitoring(self):
        """Stop tracking Redis operations"""
        self.monitor.stop_tracking()
        
    @contextmanager
    def monitor(self) -> ContextManager:
        """Context manager for monitoring Redis during test execution"""
        self.start_monitoring()
        try:
            yield self
        finally:
            self.stop_monitoring()
            self.analyzer.process_operations(self.monitor.get_operations())
            
    def get_metrics(self) -> Dict[str, Any]:
        """Get collected metrics after monitoring"""
        return {
            'hit_ratio': self.analyzer.hit_ratio,
            'operation_count': len(self.monitor.get_operations()),
            'total_time': self.analyzer.total_time,
            'data_integrity_issues': self.analyzer.data_integrity_issues
        }
        
    def validate_data_integrity(self, expected_state: Dict[str, Any]) -> bool:
        """Validate that cached values match expected application state"""
        return self.analyzer.validate_integrity(expected_state)