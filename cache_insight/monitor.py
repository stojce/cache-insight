# CacheInsight - Redis Operation Monitor
import time
from collections import defaultdict
from typing import Dict, Any, Optional

class CacheMonitor:
    def __init__(self):
        self.operation_counts = defaultdict(int)
        self.hit_count = 0
        self.miss_count = 0
        self.start_time = time.time()
        
    def track_operation(self, operation_type: str) -> None:
        """Track a Redis operation by type"""
        self.operation_counts[operation_type] += 1
        
    def record_cache_hit(self) -> None:
        """Record a cache hit"""
        self.hit_count += 1
        
    def record_cache_miss(self) -> None:
        """Record a cache miss"""
        self.miss_count += 1
        
    def get_stats(self) -> Dict[str, Any]:
        """Get current monitoring statistics"""
        total_operations = sum(self.operation_counts.values())
        total_requests = self.hit_count + self.miss_count
        hit_ratio = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        miss_ratio = (self.miss_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'total_operations': total_operations,
            'operation_breakdown': dict(self.operation_counts),
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_ratio_percent': round(hit_ratio, 2),
            'miss_ratio_percent': round(miss_ratio, 2),
            'uptime_seconds': round(time.time() - self.start_time, 2)
        }
        
    def reset(self) -> None:
        """Reset all counters to zero"""
        self.operation_counts.clear()
        self.hit_count = 0
        self.miss_count = 0
        self.start_time = time.time()