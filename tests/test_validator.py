import pytest
from cache_insight.validator import DataValidator


class TestValidator:
    @pytest.fixture
    def validator(self):
        return DataValidator()

    def test_validate_cache_integrity_matching(self, validator):
        result = validator.validate_cache_integrity("test_key", "value1", "value1")
        assert result is True

    def test_validate_cache_integrity_mismatching(self, validator, caplog):
        result = validator.validate_cache_integrity("test_key", "value1", "value2")
        assert result is False
        assert "Cache integrity violation" in caplog.text

    def test_check_for_corruption_none_value(self, validator):
        result = validator.check_for_corruption("test_key", None)
        assert result is False

    def test_check_for_corruption_large_string(self, validator, caplog):
        large_string = "a" * 60000
        result = validator.check_for_corruption("test_key", large_string)
        assert result is True
        assert "Potential corruption detected" in caplog.text

    def test_check_for_corruption_normal_string(self, validator):
        normal_string = "normal length string"
        result = validator.check_for_corruption("test_key", normal_string)
        assert result is False