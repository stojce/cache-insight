# cache_insight/monitor.py
"""Redis operation monitoring module for Cache Insight."""
import time
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
from .inspector import Inspector

class OperationTracker:
    """Tracks Redis operations and their metadata during test execution."""
    
    def __init__(self):
        self.operations: List[Dict[str, Any]] = []
        self.start_time = None
        self.end_time = None
    
    def start_recording(self):
        """Start recording Redis operations."""
        self.start_time = time.time()
        self.operations.clear()
    
    def stop_recording(self):
        """Stop recording Redis operations."""
        self.end_time = time.time()
    
    def record_operation(self, operation: str, key: str, value: Any = None, duration: float = 0):
        """Record a Redis operation with timing and metadata."""
        op_data = {
            'timestamp': time.time(),
            'operation': operation,
            'key': key,
            'value': value,
            'duration': duration,
            'thread_id': id(self)
        }
        self.operations.append(op_data)
    
    @property
    def operation_count(self) -> int:
        """Return the number of recorded operations."""
        return len(self.operations)
    
    @property
    def total_duration(self) -> float:
        """Return total time spent in Redis operations."""
        if not self.start_time or not self.end_time:
            return 0
        return self.end_time - self.start_time


class CacheMonitor:
    """Main monitor class that tracks Redis operations and provides insights."""
    
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.tracker = OperationTracker()
        self.inspector = Inspector(redis_client)
    
    @contextmanager
    def track_operations(self):
        """Context manager to track Redis operations within a specific block."""
        self.tracker.start_recording()
        try:
            yield self
        finally:
            self.tracker.stop_recording()
    
    def get_operation_stats(self) -> Dict[str, Any]:
        """Get statistics about tracked operations."""
        ops_by_type = {}
        for op in self.tracker.operations:
            op_type = op['operation']
            if op_type not in ops_by_type:
                ops_by_type[op_type] = 0
            ops_by_type[op_type] += 1
        
        return {
            'total_operations': self.tracker.operation_count,
            'operations_by_type': ops_by_type,
            'recording_duration': self.tracker.total_duration,
            'average_ops_per_second': (
                self.tracker.operation_count / self.tracker.total_duration
                if self.tracker.total_duration > 0 else 0
            )
        }