# CacheInsight - Redis-based testing tool
# Monitor module for tracking Redis operations during tests
import time
import redis
from typing import Dict, List, Optional, Any

class RedisMonitor:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.redis_client = None
        self.operation_log = []
        self.start_time = None
        
    def connect(self):
        """Establish Redis connection"""
        try:
            if self.redis_client is None:
                self.redis_client = redis.Redis(host=self.host, port=self.port, db=self.db)
            return True
        except Exception as e:
            print(f"Failed to connect to Redis: {e}")
            return False
    
    def disconnect(self):
        """Close Redis connection"""
        if self.redis_client:
            self.redis_client.close()
            self.redis_client = None
    
    def start_tracking(self):
        """Start monitoring Redis operations"""
        if not self.connect():
            return False
        
        self.start_time = time.time()
        self.operation_log = []
        return True
    
    def log_operation(self, operation_type: str, key: str, value: Any = None):
        """Log a Redis operation with timestamp"""
        if self.start_time is not None:
            timestamp = time.time() - self.start_time
            self.operation_log.append({
                'timestamp': timestamp,
                'operation': operation_type,
                'key': key,
                'value': value,
                'time': time.time()
            })
    
    def get_operations(self) -> List[Dict]:
        """Get all logged operations"""
        return self.operation_log
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about tracked operations"""
        total_ops = len(self.operation_log)
        if total_ops == 0:
            return {
                'total_operations': 0,
                'operations_by_type': {},
                'duration': 0,
                'operations_per_second': 0
            }
        
        ops_by_type = {}
        for op in self.operation_log:
            op_type = op['operation']
            if op_type in ops_by_type:
                ops_by_type[op_type] += 1
            else:
                ops_by_type[op_type] = 1
        
        duration = time.time() - self.start_time
        ops_per_sec = total_ops / duration if duration > 0 else 0
        
        return {
            'total_operations': total_ops,
            'operations_by_type': ops_by_type,
            'duration': duration,
            'operations_per_second': ops_per_sec
        }
    
    def reset(self):
        """Reset the monitor state"""
        self.operation_log = []
        self.start_time = None