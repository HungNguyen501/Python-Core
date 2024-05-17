"""Unit tests for calculate_quantile"""
import sys

import pytest
from src.common.calculate_quantile.calculate_quantile import calculate_quantile


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ([[3, 5, 99, 65, 22, 11, 22, 33], 10], 3),
        ([[3, 5, 99, 65, 22, 11, 22, 33], 22.5], 5),
        ([[3, 5, 99, 65, 22, 11, 22, 33], 45.6], 22),
        ([[3, 5, 99, 65, 22, 11, 22, 33], 50], 22),
        ([[3, 5, 99, 65, 22, 11, 22, 33], 56.3], 22),
        ([[3, 5, 99, 65, 22, 11, 22, 33], 61], 22),
        ([[3, 5, 99, 65, 22, 11, 22, 33], 75], 33),
        ([[3, 5, 99, 65, 22, 11, 22, 33], 80], 65),
        ([[3, 5, 99, 65, 22, 11, 22, 33], 95], 99),
        ([[3, 5, 99, 65, 22, 11, 22, 33], 99.5], 99),
    ]
)
def test_calculate_quantile(test_input, expected):
    """Test function calculate_quantile"""
    assert calculate_quantile(*test_input) == expected


def test_calculate_quantile_with_value_error():
    """Test function calculate_quantile with
    percentile be out of range [0, 100]
    """
    with pytest.raises(ValueError):
        calculate_quantile([1, 3, 4], 150)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__] + sys.argv[1:]))
