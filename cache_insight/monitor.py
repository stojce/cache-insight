# CacheInsight - Redis Operation Monitor
import time
import asyncio
from typing import Dict, List, Optional, Any, Callable
from collections import defaultdict


class CacheMonitor:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Reset all monitoring statistics."""
        self._operations = []
        self._start_time = None
        self._end_time = None
        self._operation_counts = {
            'GET': 0,
            'SET': 0,
            'DEL': 0,
            'HGET': 0,
            'HSET': 0,
            'EXISTS': 0,
            'OTHER': 0
        }
        self._key_access_patterns = defaultdict(int)
        self._hit_count = 0
        self._miss_count = 0
        
    def start_capture(self):
        """Start capturing Redis operations."""
        self.reset()
        self._start_time = time.time()
        
    def stop_capture(self):
        """Stop capturing Redis operations."""
        self._end_time = time.time()
        
    def record_operation(self, command: str, key: str, result: Any = None, duration: float = 0):
        """Record a Redis operation with its result and timing."""
        op_data = {
            'timestamp': time.time(),
            'command': command.upper(),
            'key': key,
            'result': result,
            'duration': duration
        }
        self._operations.append(op_data)
        
        # Count the operation
        if op_data['command'] in self._operation_counts:
            self._operation_counts[op_data['command']] += 1
        else:
            self._operation_counts['OTHER'] += 1
            
        # Track key access patterns
        self._key_access_patterns[key] += 1
        
        # Track hits/misses for GET operations
        if command.upper() == 'GET' or command.upper().startswith('HGET'):
            if result is not None:
                self._hit_count += 1
            else:
                self._miss_count += 1
    
    @property
    def operations(self) -> List[Dict[str, Any]]:
        """Get list of captured operations."""
        return self._operations.copy()
        
    @property
    def total_operations(self) -> int:
        """Get total number of operations performed."""
        return len(self._operations)
        
    @property
    def duration(self) -> float:
        """Get the duration of monitoring in seconds."""
        if self._start_time is not None and self._end_time is not None:
            return self._end_time - self._start_time
        return 0
        
    @property
    def operation_counts(self) -> Dict[str, int]:
        """Get counts for each type of operation."""
        return self._operation_counts.copy()
        
    @property
    def hit_ratio(self) -> float:
        """Calculate cache hit ratio."""
        total = self._hit_count + self._miss_count
        if total == 0:
            return 0.0
        return self._hit_count / total
        
    @property
    def miss_ratio(self) -> float:
        """Calculate cache miss ratio."""
        total = self._hit_count + self._miss_count
        if total == 0:
            return 0.0
        return self._miss_count / total
        
    @property
    def hit_count(self) -> int:
        """Get number of cache hits."""
        return self._hit_count
        
    @property
    def miss_count(self) -> int:
        """Get number of cache misses."""
        return self._miss_count
        
    def get_top_keys(self, n: int = 10) -> List[tuple]:
        """Get top N most accessed keys."""
        sorted_keys = sorted(
            self._key_access_patterns.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return sorted_keys[:n]
        
    def __enter__(self):
        """Context manager entry - start capture."""
        self.start_capture()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - stop capture."""
        self.stop_capture()
        
    async def __aenter__(self):
        """Async context manager entry - start capture."""
        self.start_capture()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - stop capture."""
        self.stop_capture()