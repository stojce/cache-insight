import unittest
from cache_insight.monitor import Monitor

class TestMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = Monitor()
        
    def test_initialization(self):
        self.assertEqual(len(self.monitor.get_tracked_operations()), 0)
        self.assertEqual(len(self.monitor.listeners), 0)
        
    def test_start_stop_monitoring(self):
        self.monitor.start_monitoring()
        self.monitor.stop_monitoring()
        # Verify cleanup happened
        self.assertEqual(len(self.monitor.listeners), 0)
        
    def test_register_listener(self):
        class MockListener:
            def cleanup(self):
                pass
        
        self.monitor.register_listener(MockListener())
        self.assertEqual(len(self.monitor.listeners), 1)
        
    def test_cleanup_listeners(self):
        class MockListener:
            def __init__(self):
                self.cleaned_up = False
            
            def cleanup(self):
                self.cleaned_up = True
        
        listener = MockListener()
        self.monitor.register_listener(listener)
        self.monitor._cleanup_listeners()
        self.assertTrue(listener.cleaned_up)
        self.assertEqual(len(self.monitor.listeners), 0)
        
    def test_reset(self):
        self.monitor.tracked_operations = ["op1", "op2"]
        self.monitor.reset()
        self.assertEqual(len(self.monitor.get_tracked_operations()), 0)