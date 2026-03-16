import pytest
from unittest.mock import Mock, patch
from cache_insight.validator import CacheValidator


def test_validate_integrity_success():
    mock_redis = Mock()
    mock_redis.get.return_value = b'test_value'
    validator = CacheValidator(mock_redis)
    
    result = validator.validate_integrity('test_key', 'test_value')
    assert result is True
    mock_redis.get.assert_called_once_with('test_key')


def test_validate_integrity_failure():
    mock_redis = Mock()
    mock_redis.get.return_value = b'wrong_value'
    validator = CacheValidator(mock_redis)
    
    result = validator.validate_integrity('test_key', 'test_value')
    assert result is False


def test_validate_integrity_missing_key():
    mock_redis = Mock()
    mock_redis.get.return_value = None
    validator = CacheValidator(mock_redis)
    
    result = validator.validate_integrity('missing_key', 'test_value')
    assert result is False


def test_validate_integrity_number_types():
    mock_redis = Mock()
    mock_redis.get.return_value = b'42'
    validator = CacheValidator(mock_redis)
    
    # Test integer
    result = validator.validate_integrity('num_key', 42)
    assert result is True
    
    # Test float
    mock_redis.get.return_value = b'42.5'
    result = validator.validate_integrity('float_key', 42.5)
    assert result is True


def test_validate_integrity_invalid_number():
    mock_redis = Mock()
    mock_redis.get.return_value = b'not_a_number'
    validator = CacheValidator(mock_redis)
    
    result = validator.validate_integrity('invalid_num_key', 42)
    assert result is False


def test_batch_validate():
    mock_redis = Mock()
    
    def mock_get(key):
        if key == 'key1':
            return b'value1'
        elif key == 'key2':
            return b'value2'
        else:
            return None
    
    mock_redis.get.side_effect = mock_get
    validator = CacheValidator(mock_redis)
    
    validations = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3'  # This will be missing from cache
    }
    
    results = validator.batch_validate(validations)
    assert results == {
        'key1': True,
        'key2': True,
        'key3': False
    }


def test_validate_integrity_with_json():
    mock_redis = Mock()
    import json
    test_data = {'name': 'test', 'id': 123}
    mock_redis.get.return_value = json.dumps(test_data).encode()
    validator = CacheValidator(mock_redis)
    
    result = validator.validate_integrity('json_key', test_data)
    assert result is True


def test_validate_integrity_error_handling():
    mock_redis = Mock()
    mock_redis.get.side_effect = Exception("Redis connection failed")
    validator = CacheValidator(mock_redis)
    
    result = validator.validate_integrity('any_key', 'any_value')
    assert result is False
