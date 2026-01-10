# Cache Inspector Module
import redis
import time
from typing import Dict, Any, Optional

class RedisInspector:
    def __init__(self, connection_string: str):
        self.connection = redis.from_url(connection_string)
        self.operation_log = []
        self._tracked_keys = set()
    
    def start_tracking(self):
        """Initialize tracking and record starting state"""
        self._clear_existing_listeners()
        self.operation_log.clear()
        self._tracked_keys.clear()
        
    def _clear_existing_listeners(self):
        """Remove any existing pubsub listeners to prevent accumulation"""
        if hasattr(self, '_pubsub') and self._pubsub:
            self._pubsub.close()
        self._pubsub = self.connection.pubsub()
    
    def track_operations(self, duration: int = 30):
        """Listen for Redis commands for the specified duration"""
        self._pubsub.psubscribe('__keyspace@*__:*')
        start_time = time.time()
        
        while time.time() - start_time < duration:
            message = self._pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                self.operation_log.append({
                    'time': time.time(),
                    'channel': message['channel'],
                    'data': message['data']
                })
            time.sleep(0.01)  # Prevent excessive CPU usage
    
    def get_tracked_operations(self) -> list:
        """Return collected operations"""
        return self.operation_log.copy()
    
    def add_tracked_key(self, key: str):
        """Add a key to be monitored for changes"""
        self._tracked_keys.add(key)
    
    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, '_pubsub') and self._pubsub:
            self._pubsub.close()
        self.operation_log.clear()
        self._tracked_keys.clear()