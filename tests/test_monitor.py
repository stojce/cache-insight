import unittest
from cache_insight.monitor import CacheMonitor

class TestCacheMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = CacheMonitor()
    
    def test_initial_stats(self):
        stats = self.monitor.get_stats()
        self.assertEqual(stats['operation_count'], 0)
        self.assertEqual(stats['get_operations'], 0)
        self.assertEqual(stats['set_operations'], 0)
        self.assertEqual(stats['hit_count'], 0)
        self.assertEqual(stats['miss_count'], 0)
        self.assertEqual(stats['hit_ratio_percent'], 0.0)
        self.assertEqual(stats['miss_ratio_percent'], 0.0)
    
    def test_track_get_operation_hit(self):
        self.monitor.track_operation('get', 'key1', exists=True)
        stats = self.monitor.get_stats()
        self.assertEqual(stats['get_operations'], 1)
        self.assertEqual(stats['hit_count'], 1)
        self.assertEqual(stats['miss_count'], 0)
        self.assertEqual(stats['hit_ratio_percent'], 100.0)
    
    def test_track_get_operation_miss(self):
        self.monitor.track_operation('get', 'key1', exists=False)
        stats = self.monitor.get_stats()
        self.assertEqual(stats['get_operations'], 1)
        self.assertEqual(stats['miss_count'], 1)
        self.assertEqual(stats['hit_count'], 0)
        self.assertEqual(stats['miss_ratio_percent'], 100.0)
    
    def test_track_mixed_operations(self):
        # 2 hits and 2 misses
        self.monitor.track_operation('get', 'key1', exists=True)
        self.monitor.track_operation('get', 'key2', exists=False)
        self.monitor.track_operation('get', 'key3', exists=True)
        self.monitor.track_operation('get', 'key4', exists=False)
        
        stats = self.monitor.get_stats()
        self.assertEqual(stats['get_operations'], 4)
        self.assertEqual(stats['hit_count'], 2)
        self.assertEqual(stats['miss_count'], 2)
        self.assertEqual(stats['hit_ratio_percent'], 50.0)
        self.assertEqual(stats['miss_ratio_percent'], 50.0)
    
    def test_track_set_operation(self):
        self.monitor.track_operation('set', 'key1', 'value1')
        stats = self.monitor.get_stats()
        self.assertEqual(stats['set_operations'], 1)
        self.assertEqual(stats['get_operations'], 0)
    
    def test_reset_stats(self):
        self.monitor.track_operation('get', 'key1', exists=True)
        self.monitor.reset_stats()
        
        stats = self.monitor.get_stats()
        self.assertEqual(stats['operation_count'], 0)
        self.assertEqual(stats['get_operations'], 0)
        self.assertEqual(stats['set_operations'], 0)
        self.assertEqual(stats['hit_count'], 0)
        self.assertEqual(stats['miss_count'], 0)
