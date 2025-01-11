# CacheInsight Monitor
# Handles real-time monitoring of Redis operations
import time
from collections import defaultdict

class Monitor:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Reset all monitoring statistics"""
        self.stats = {
            'operations': [],
            'hit_count': 0,
            'miss_count': 0,
            'start_time': time.time(),
            'listeners': []  # Track registered listeners
        }
        
    def register_listener(self, callback):
        """Register a callback to receive operation events"""
        self.stats['listeners'].append(callback)
        return len(self.stats['listeners']) - 1
    
    def remove_listener(self, listener_id):
        """Remove a listener by ID"""
        if 0 <= listener_id < len(self.stats['listeners']):
            del self.stats['listeners'][listener_id]
    
    def track_operation(self, op_type, key, value=None, hit_status=None):
        """Record a Redis operation with timestamp and metadata"""
        op = {
            'timestamp': time.time(),
            'type': op_type,
            'key': key,
            'value': value,
            'hit': hit_status
        }
        self.stats['operations'].append(op)
        
        # Update hit/miss counts
        if hit_status is True:
            self.stats['hit_count'] += 1
        elif hit_status is False:
            self.stats['miss_count'] += 1
        
        # Notify all registered listeners
        for listener in list(self.stats['listeners']):  # Use copy to prevent modification during iteration
            try:
                listener(op)
            except Exception as e:
                print(f"Error in monitor listener: {e}")
    
    def get_hit_ratio(self):
        """Calculate the cache hit ratio"""
        total = self.stats['hit_count'] + self.stats['miss_count']
        if total == 0:
            return 0.0
        return self.stats['hit_count'] / total
    
    def get_stats(self):
        """Return current monitoring statistics"""
        duration = time.time() - self.stats['start_time']
        return {
            'duration': duration,
            'total_operations': len(self.stats['operations']),
            'hit_count': self.stats['hit_count'],
            'miss_count': self.stats['miss_count'],
            'hit_ratio': self.get_hit_ratio(),
            'operations': self.stats['operations'][-100:]  # Return last 100 ops to avoid memory issues
        }