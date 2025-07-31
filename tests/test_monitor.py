import pytest
import asyncio
from unittest.mock import Mock
from cache_insight.monitor import RedisMonitor

def test_monitor_context_manager():
    # Create a mock Redis client
    mock_redis = Mock()
    monitor = RedisMonitor(mock_redis)
    
    async def run_test():
        async with monitor as m:
            # Perform some operations
            m.record_operation('GET', 'test_key', True, 50)
            m.record_operation('SET', 'test_key', True, 50)
            m.record_operation('GET', 'missing_key', False)
            
        # Verify metrics after context exit
        metrics = m.get_performance_metrics()
        assert metrics['hit_count'] == 1
        assert metrics['miss_count'] == 1
        assert metrics['total_operations'] == 3
        
    asyncio.run(run_test())

def test_monitor_operations_tracking():
    mock_redis = Mock()
    monitor = RedisMonitor(mock_redis)
    
    monitor.start_monitoring()
    monitor.record_operation('GET', 'key1', True, 100)
    monitor.record_operation('SET', 'key2', True, 80)
    monitor.record_operation('GET', 'key3', True, 60)
    monitor.stop_monitoring()
    
    metrics = monitor.get_performance_metrics()
    assert metrics['hit_count'] == 2
    assert metrics['miss_count'] == 0
    assert metrics['hit_ratio'] == 1.0
    
    ops = monitor.operation_stats
    assert ops['GET'] == 2
    assert ops['SET'] == 1