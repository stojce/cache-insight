# CacheInsight Monitor
# Handles real-time Redis operation tracking during test execution
import asyncio
import time
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque

class RedisMonitor:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.operations = deque()
        self.hit_count = 0
        self.miss_count = 0
        self.operation_stats = defaultdict(int)
        self._is_active = False
        
    async def __aenter__(self):
        self.start_monitoring()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.stop_monitoring()
        
    def start_monitoring(self):
        """Start monitoring Redis operations"""
        self._is_active = True
        # In a real implementation, we would hook into Redis commands here
        self.start_time = time.time()
        print("Redis monitoring started")
        
    def stop_monitoring(self):
        """Stop monitoring Redis operations"""
        self._is_active = False
        self.end_time = time.time()
        print(f"Redis monitoring stopped. Duration: {self.end_time - self.start_time:.2f}s")
        
    def record_operation(self, op_type: str, key: str, success: bool = True, value_size: int = 0):
        """Record a Redis operation"""
        if not self._is_active:
            return
            
        operation = {
            'timestamp': time.time(),
            'op_type': op_type,
            'key': key,
            'success': success,
            'value_size': value_size
        }
        self.operations.append(operation)
        self.operation_stats[op_type] += 1
        
        if op_type == 'GET' and success:
            self.hit_count += 1
        elif op_type == 'GET' and not success:
            self.miss_count += 1
            
    def get_hit_ratio(self) -> float:
        """Calculate the cache hit ratio"""
        total_requests = self.hit_count + self.miss_count
        if total_requests == 0:
            return 0.0
        return self.hit_count / total_requests
        
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        total_requests = self.hit_count + self.miss_count
        duration = self.end_time - self.start_time if hasattr(self, 'end_time') else time.time() - self.start_time
        
        return {
            'hit_ratio': self.get_hit_ratio(),
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'total_operations': len(self.operations),
            'operation_types': dict(self.operation_stats),
            'duration_seconds': duration,
            'ops_per_second': len(self.operations) / duration if duration > 0 else 0
        }