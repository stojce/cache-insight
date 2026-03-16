# Cache Insight - Validator Module
# Validates data integrity between application state and cached values

import logging
from typing import Any, Dict, Optional
from redis import Redis


class CacheValidator:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.logger = logging.getLogger(__name__)

    def validate_integrity(self, key: str, expected_value: Any) -> bool:
        """
        Validate that the cached value matches the expected application state.
        
        Args:
            key: The cache key to validate
            expected_value: The expected value from application state
            
        Returns:
            True if values match, False otherwise
        """
        try:
            cached_value = self.redis_client.get(key)
            if cached_value is None:
                self.logger.warning(f"Key {key} not found in cache")
                return False
            
            # Handle string representation of non-string values
            if isinstance(expected_value, (int, float)):
                try:
                    if isinstance(expected_value, int):
                        return int(cached_value.decode()) == expected_value
                    else:
                        return float(cached_value.decode()) == expected_value
                except ValueError:
                    self.logger.error(f"Could not convert cached value to number for key {key}")
                    return False
            elif isinstance(expected_value, str):
                return cached_value.decode() == expected_value
            else:
                # For complex objects, compare string representations
                import json
                try:
                    cached_as_json = json.loads(cached_value.decode())
                    expected_as_json = json.loads(json.dumps(expected_value))
                    return cached_as_json == expected_as_json
                except (ValueError, TypeError):
                    self.logger.error(f"Could not serialize objects for comparison for key {key}")
                    return False
        except Exception as e:
            self.logger.error(f"Error validating cache integrity for key {key}: {str(e)}")
            return False

    def batch_validate(self, validations: Dict[str, Any]) -> Dict[str, bool]:
        """
        Validate multiple keys at once.
        
        Args:
            validations: Dictionary mapping keys to expected values
            
        Returns:
            Dictionary mapping keys to validation results
        """
        results = {}
        for key, expected_value in validations.items():
            results[key] = self.validate_integrity(key, expected_value)
        return results
