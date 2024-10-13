"""Data manager"""
from functools import cache

from .models.pool_entity import PoolEntity


@cache
class DataManager:  # pylint: disable=too-few-public-methods
    """Data Manager"""
    def __init__(self,):
        """Init Data manager"""
        self.pool_entity = PoolEntity(pools={})

    def get_pools(self,) -> dict:
        """Returns pool"""
        return self.pool_entity.pools


def generate_pools():
    """Returns DataManager along with new PoolEntity"""
    return DataManager()
