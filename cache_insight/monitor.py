# CacheInsight Monitor
# Handles real-time monitoring of Redis operations

import asyncio
import aioredis
import time
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque

class CacheMonitor:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_pool = None
        self.operation_history = deque(maxlen=1000)
        self.metrics = {
            'hits': 0,
            'misses': 0,
            'total_operations': 0,
            'operation_times': []
        }
        self.active_operations = {}

    async def connect(self):
        """Initialize Redis connection pool"""
        if not self.redis_pool:
            self.redis_pool = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=20,
                min_connections=5
            )

    async def disconnect(self):
        """Close Redis connection pool"""
        if self.redis_pool:
            await self.redis_pool.close()
            await self.redis_pool.connection_pool.disconnect()
            self.redis_pool = None

    async def start_tracking(self):
        """Begin tracking Redis operations"""
        await self.connect()
        print("Cache monitoring started...")

    async def stop_tracking(self):
        """Stop tracking Redis operations"""
        await self.disconnect()
        print("Cache monitoring stopped.")

    async def execute_operation(self, operation: str, key: str, value: Any = None) -> Any:
        """Execute a Redis operation and track it"""
        start_time = time.time()
        
        try:
            if operation == "GET":
                result = await self.redis_pool.get(key)
                if result is not None:
                    self.metrics['hits'] += 1
                else:
                    self.metrics['misses'] += 1
                return result
            elif operation == "SET":
                result = await self.redis_pool.set(key, value)
                return result
            elif operation == "DEL":
                result = await self.redis_pool.delete(key)
                return result
            elif operation == "EXISTS":
                result = await self.redis_pool.exists(key)
                return bool(result)
            else:
                raise ValueError(f"Unsupported operation: {operation}")
        finally:
            end_time = time.time()
            duration = end_time - start_time
            self.metrics['total_operations'] += 1
            self.metrics['operation_times'].append(duration)
            
            # Log the operation
            op_record = {
                'timestamp': time.time(),
                'operation': operation,
                'key': key,
                'value': str(value)[:50] + "..." if value and len(str(value)) > 50 else str(value),
                'duration': duration
            }
            self.operation_history.append(op_record)

    def get_metrics(self) -> Dict[str, Any]:
        """Get current cache performance metrics"""
        total_ops = self.metrics['total_operations']
        if total_ops == 0:
            hit_ratio = 0
            miss_ratio = 0
        else:
            hit_ratio = self.metrics['hits'] / total_ops
            miss_ratio = self.metrics['misses'] / total_ops
        
        avg_duration = sum(self.metrics['operation_times']) / len(self.metrics['operation_times']) if self.metrics['operation_times'] else 0
        
        return {
            'hit_ratio': hit_ratio,
            'miss_ratio': miss_ratio,
            'total_operations': total_ops,
            'hits': self.metrics['hits'],
            'misses': self.metrics['misses'],
            'average_response_time': avg_duration,
            'operations_per_second': self._calculate_ops_per_second()
        }
    
    def _calculate_ops_per_second(self) -> float:
        """Calculate operations per second based on recent activity"""
        if not self.operation_history:
            return 0
        
        # Look at last 30 seconds of operations
        recent_threshold = time.time() - 30
        recent_ops = [op for op in self.operation_history if op['timestamp'] > recent_threshold]
        return len(recent_ops) / 30 if len(recent_ops) > 0 else 0

    def reset_metrics(self):
        """Reset all metrics to initial state"""
        self.metrics = {
            'hits': 0,
            'misses': 0,
            'total_operations': 0,
            'operation_times': []
        }
        self.operation_history.clear()
