# Redis monitoring module
import redis
import time
from typing import Dict, Any, Optional

class CacheMonitor:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.redis_client = None
        self.operation_log = []
        self.metrics = {
            'get_count': 0,
            'set_count': 0,
            'del_count': 0,
            'hit_count': 0,
            'miss_count': 0,
            'start_time': time.time()
        }

    def connect(self) -> bool:
        try:
            self.redis_client = redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True)
            # Test the connection
            self.redis_client.ping()
            return True
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error connecting to Redis: {e}")
            return False

    def log_operation(self, op_type: str, key: str, value: Optional[str] = None, hit_status: Optional[bool] = None):
        timestamp = time.time()
        entry = {
            'timestamp': timestamp,
            'operation': op_type,
            'key': key,
            'value': value,
            'hit': hit_status
        }
        self.operation_log.append(entry)
        
        # Update metrics based on operation type
        if op_type == 'GET':
            self.metrics['get_count'] += 1
            if hit_status is True:
                self.metrics['hit_count'] += 1
            elif hit_status is False:
                self.metrics['miss_count'] += 1
        elif op_type == 'SET':
            self.metrics['set_count'] += 1
        elif op_type == 'DEL':
            self.metrics['del_count'] += 1

    def get_cache_stats(self) -> Dict[str, Any]:
        total_requests = self.metrics['get_count']
        hits = self.metrics['hit_count']
        misses = self.metrics['miss_count']
        
        hit_rate = (hits / total_requests * 100) if total_requests > 0 else 0
        miss_rate = (misses / total_requests * 100) if total_requests > 0 else 0
        
        stats = {
            'total_gets': total_requests,
            'total_sets': self.metrics['set_count'],
            'total_dels': self.metrics['del_count'],
            'hits': hits,
            'misses': misses,
            'hit_rate_percent': round(hit_rate, 2),
            'miss_rate_percent': round(miss_rate, 2),
            'duration_seconds': round(time.time() - self.metrics['start_time'], 2)
        }
        return stats

    def reset(self):
        self.operation_log = []
        self.metrics = {
            'get_count': 0,
            'set_count': 0,
            'del_count': 0,
            'hit_count': 0,
            'miss_count': 0,
            'start_time': time.time()
        }