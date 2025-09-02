# CacheInsight - Redis Validation Module
import logging
from typing import Dict, Any, Optional, List
from redis import Redis


class DataValidator:
    """Validates data integrity between application state and cached values."""
    
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.logger = logging.getLogger(__name__)
        
    def validate_integrity(self, expected_data: Dict[str, Any], keys_to_check: List[str]) -> Dict[str, Any]:
        """Validate that cached values match expected application state.
        
        Args:
            expected_data: Dictionary mapping keys to expected values
            keys_to_check: List of keys to validate
            
        Returns:
            Dictionary containing validation results
        """
        try:
            validation_results = {
                'valid': True,
                'mismatches': [],
                'missing_keys': [],
                'errors': []
            }
            
            for key in keys_to_check:
                if key not in expected_data:
                    validation_results['missing_keys'].append(key)
                    continue
                    
                try:
                    cached_value = self.redis_client.get(key)
                    expected_value = expected_data[key]
                    
                    if cached_value != expected_value:
                        validation_results['mismatches'].append({
                            'key': key,
                            'expected': expected_value,
                            'actual': cached_value,
                            'type': 'value_mismatch'
                        })
                        validation_results['valid'] = False
                except Exception as e:
                    validation_results['errors'].append({
                        'key': key,
                        'error': str(e),
                        'type': 'validation_error'
                    })
                    validation_results['valid'] = False
                    self.logger.error(f"Error validating key {key}: {e}")
                    
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Unexpected error during validation: {e}")
            return {
                'valid': False,
                'mismatches': [],
                'missing_keys': [],
                'errors': [{'error': str(e), 'type': 'unexpected_error'}]
            }
            
    def get_validation_summary(self, results: Dict[str, Any]) -> str:
        """Generate a human-readable summary of validation results."""
        if results['valid']:
            return "All cache validations passed successfully."
        else:
            summary = "Validation failures detected:\n"
            if results['mismatches']:
                summary += f"  - {len(results['mismatches'])} value mismatches\n"
            if results['missing_keys']:
                summary += f"  - {len(results['missing_keys'])} missing keys in expected data\n"
            if results['errors']:
                summary += f"  - {len(results['errors'])} validation errors\n"
            return summary