# Tests for CacheMonitor
def test_monitor_initialization():
    from cache_insight.monitor import CacheMonitor
    monitor = CacheMonitor()
    assert monitor.hit_count == 0
    assert monitor.miss_count == 0
    assert monitor.operation_count == 0
    assert len(monitor.operations_log) == 0

def test_record_cache_hit():
    from cache_insight.monitor import CacheMonitor
    monitor = CacheMonitor()
    monitor.record_cache_hit("test_key")
    assert monitor.hit_count == 1
    assert monitor.operation_count == 1
    assert monitor.operations_log[0]['operation'] == 'GET'
    assert monitor.operations_log[0]['key'] == 'test_key'

def test_record_cache_miss():
    from cache_insight.monitor import CacheMonitor
    monitor = CacheMonitor()
    monitor.record_cache_miss("test_key")
    assert monitor.miss_count == 1
    assert monitor.operation_count == 1
    assert monitor.operations_log[0]['operation'] == 'MISS'
    assert monitor.operations_log[0]['key'] == 'test_key'

def test_hit_ratio_calculation():
    from cache_insight.monitor import CacheMonitor
    monitor = CacheMonitor()
    # No operations - ratio should be 0
    assert monitor.get_hit_ratio() == 0.0
    
    # 5 hits, 0 misses - ratio should be 1.0
    for i in range(5):
        monitor.record_cache_hit(f"key{i}")
    assert monitor.get_hit_ratio() == 1.0
    
    # 7 hits, 8 misses - ratio should be 0.4666...
    for i in range(8):
        monitor.record_cache_miss(f"miss_key{i}")
    expected_ratio = 5 / (5 + 8)
    assert abs(monitor.get_hit_ratio() - expected_ratio) < 0.001