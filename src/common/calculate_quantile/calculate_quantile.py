"""Calculate quantile of an array"""
from math import ceil
from typing import List


def calculate_quantile(arr: List[int], percentile: float):
    """
    Return calculated quantile of list
    Args:
        arr(list): array of integer numbers
        percentile(float): percentile value
    """
    if percentile < 0 or percentile > 100:
        raise ValueError("Percentile must be in range [0, 100]")
    sorted_arr = sorted(arr)
    index = ceil(percentile/100 * len(sorted_arr)) - 1
    return sorted_arr[index]
