# cache_insight/validator.py
import hashlib
import json
from typing import Any, Dict, Optional
from .monitor import Monitor

class CacheIntegrityValidator:
    """
    Validates cache integrity by comparing application state
    with cached values to ensure data consistency.
    """
    
    def __init__(self, monitor: Monitor):
        self.monitor = monitor
        self.integrity_checks = []
    
    def add_check(self, key: str, expected_value: Any, namespace: str = "default") -> None:
        """
        Adds a cache integrity check for a specific key-value pair.
        
        Args:
            key: The cache key to validate
            expected_value: The expected value in the application state
            namespace: Grouping identifier for related checks
        """
        check_id = hashlib.md5(f"{namespace}:{key}".encode()).hexdigest()
        self.integrity_checks.append({
            "id": check_id,
            "key": key,
            "expected": expected_value,
            "namespace": namespace
        })
    
    def validate_all(self) -> Dict[str, Any]:
        """
        Runs all integrity checks and returns results.
        
        Returns:
            Dictionary containing validation summary and details
        """
        results = {
            "total_checks": len(self.integrity_checks),
            "passed_checks": 0,
            "failed_checks": 0,
            "checks": []
        }
        
        for check in self.integrity_checks:
            cached_value = self._get_cached_value(check["key"])
            is_valid = self._compare_values(cached_value, check["expected"])
            
            result = {
                "id": check["id"],
                "key": check["key"],
                "status": "PASS" if is_valid else "FAIL",
                "expected": check["expected"],
                "actual": cached_value
            }
            
            results["checks"].append(result)
            
            if is_valid:
                results["passed_checks"] += 1
            else:
                results["failed_checks"] += 1
        
        return results
    
    def _get_cached_value(self, key: str) -> Optional[Any]:
        """Retrieves the cached value from the Redis instance."""
        try:
            redis_client = self.monitor.get_redis_client()
            value = redis_client.get(key)
            if value is not None:
                return json.loads(value.decode('utf-8'))
            return None
        except Exception as e:
            print(f"Error retrieving cached value for key {key}: {e}")
            return None
    
    def _compare_values(self, cached: Any, expected: Any) -> bool:
        """Compares cached and expected values for equality."""
        try:
            return json.dumps(cached, sort_keys=True) == json.dumps(expected, sort_keys=True)
        except:
            return cached == expected