# CacheInsight Monitor
# Handles real-time monitoring of Redis operations

class Monitor:
    def __init__(self):
        self.tracked_operations = []
        self.listeners = []
        
    def start_monitoring(self):
        """Begin monitoring Redis operations"""
        print("Starting Redis monitoring...")
        
    def stop_monitoring(self):
        """Stop monitoring and cleanup resources"""
        print("Stopping Redis monitoring...")
        self._cleanup_listeners()
        
    def _cleanup_listeners(self):
        """Clean up registered event listeners to prevent memory leaks"""
        for listener in self.listeners:
            try:
                listener.cleanup()
            except AttributeError:
                pass  # Listener doesn't have cleanup method
        self.listeners.clear()
        
    def register_listener(self, listener):
        """Register a listener for Redis events"""
        self.listeners.append(listener)
        
    def get_tracked_operations(self):
        """Return list of tracked operations"""
        return self.tracked_operations
        
    def reset(self):
        """Reset the monitor state"""
        self.tracked_operations = []
        self._cleanup_listeners()