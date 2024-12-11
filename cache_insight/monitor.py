# CacheInsight Monitor
# Tracks Redis operations during test execution

class CacheMonitor:
    def __init__(self):
        self.reset_stats()
    
    def reset_stats(self):
        """Reset all monitoring statistics"""
        self.operation_count = 0
        self.get_operations = 0
        self.set_operations = 0
        self.hit_count = 0
        self.miss_count = 0
        self.cache_size = 0
    
    def track_operation(self, op_type, key, value=None, exists=False):
        """Track a Redis operation
        
        Args:
            op_type (str): Type of operation ('get', 'set', etc.)
            key (str): The cache key being operated on
            value: The value associated with the operation
            exists (bool): For GET operations, whether key existed
        """
        self.operation_count += 1
        
        if op_type == 'get':
            self.get_operations += 1
            if exists:
                self.hit_count += 1
            else:
                self.miss_count += 1
        elif op_type == 'set':
            self.set_operations += 1
    
    def get_hit_ratio(self):
        """Calculate the cache hit ratio as a percentage"""
        if self.get_operations == 0:
            return 0.0
        return (self.hit_count / self.get_operations) * 100
    
    def get_miss_ratio(self):
        """Calculate the cache miss ratio as a percentage"""
        if self.get_operations == 0:
            return 0.0
        return (self.miss_count / self.get_operations) * 100
    
    def get_stats(self):
        """Get current monitoring statistics"""
        return {
            'operation_count': self.operation_count,
            'get_operations': self.get_operations,
            'set_operations': self.set_operations,
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_ratio_percent': round(self.get_hit_ratio(), 2),
            'miss_ratio_percent': round(self.get_miss_ratio(), 2)
        }
