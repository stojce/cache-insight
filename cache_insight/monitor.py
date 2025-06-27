# CacheInsight Monitor
# Tracks Redis operations during test execution

class CacheMonitor:
    def __init__(self):
        self.reset_stats()
    
    def reset_stats(self):
        """Reset all monitoring statistics"""
        self.hit_count = 0
        self.miss_count = 0
        self.operation_count = 0
        self.operations_log = []
    
    def record_operation(self, operation_type, key, success=True):
        """Record a Redis operation"""
        self.operation_count += 1
        self.operations_log.append({
            'operation': operation_type,
            'key': key,
            'success': success,
            'timestamp': self._get_timestamp()
        })
    
    def record_cache_hit(self, key):
        """Record a cache hit"""
        self.hit_count += 1
        self.record_operation('GET', key, True)
    
    def record_cache_miss(self, key):
        """Record a cache miss"""
        self.miss_count += 1
        self.record_operation('MISS', key, False)
    
    def get_hit_ratio(self):
        """Calculate and return the cache hit ratio"""
        total = self.hit_count + self.miss_count
        if total == 0:
            return 0.0
        return self.hit_count / total
    
    def get_stats(self):
        """Return current monitoring statistics"""
        return {
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'total_operations': self.operation_count,
            'hit_ratio': self.get_hit_ratio(),
            'operations_log': self.operations_log.copy()
        }
    
    def _get_timestamp(self):
        import time
        return time.time()