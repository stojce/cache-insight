# CacheInsight - Redis Validation Module
import logging
from typing import Dict, Any, Optional, List
from redis import Redis


class CacheValidator:
    """Validates data integrity between application state and cached values"""
    
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.logger = logging.getLogger(__name__)
        
    def validate_data_integrity(self, key_mapping: Dict[str, Any]) -> Dict[str, bool]:
        """Validate that cached values match expected application state"""
        results = {}
        
        for key, expected_value in key_mapping.items():
            try:
                cached_value = self.redis_client.get(key)
                if cached_value is None:
                    results[key] = False
                    self.logger.warning(f"Key {key} not found in cache")
                    continue
                    
                # Handle different value types appropriately
                if isinstance(expected_value, (int, float)):
                    try:
                        cached_as_numeric = float(cached_value)
                        results[key] = abs(expected_value - cached_as_numeric) < 1e-9
                    except ValueError:
                        results[key] = False
                        self.logger.error(f"Failed to convert cached value to numeric for key {key}")
                elif isinstance(expected_value, str):
                    results[key] = cached_value.decode('utf-8') == expected_value
                else:
                    results[key] = cached_value == expected_value
                    
                if not results[key]:
                    self.logger.warning(f"Data integrity violation for key {key}: expected {expected_value}, got {cached_value}")
            
            except Exception as e:
                results[key] = False
                self.logger.error(f"Error validating key {key}: {str(e)}")
        
        return results
        
    def check_missing_keys(self, expected_keys: List[str]) -> List[str]:
        """Check which keys from expected list are missing in cache"""
        missing = []
        for key in expected_keys:
            try:
                if not self.redis_client.exists(key):
                    missing.append(key)
            except Exception as e:
                self.logger.error(f"Error checking existence of key {key}: {str(e)}")
        return missing
        
    def get_validation_summary(self, results: Dict[str, bool]) -> Dict[str, int]:
        """Return summary statistics for validation results"""
        total = len(results)
        passed = sum(1 for v in results.values() if v)
        failed = total - passed
        
        return {
            "total_validations": total,
            "passed": passed,
            "failed": failed,
            "success_rate": passed / total if total > 0 else 0
        }