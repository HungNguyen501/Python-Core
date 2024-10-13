"""Pool service"""
from typing import List

from fastapi import Depends
from src.pool_api.repositories import DataManager, generate_pools
from src.common.calculate_quantile.calculate_quantile import calculate_quantile


class PoolService:
    """Pool Service"""
    db: DataManager

    def __init__(self, db: DataManager = Depends(generate_pools)) -> None:
        """Constructor"""
        self.db = db

    def _get_pools(self,):
        """Returns pools"""
        return self.db.get_pools()

    def upsert_pool(self, pool_id: int, values: List[int]):
        """Upsert values for pool"""
        pools = self._get_pools()
        if pool := pools.get(pool_id):
            pool.extend(values)
            return "appended"
        pools[pool_id] = values
        return "inserted"

    def calculate_quantile(self, pool_id: int, percentile: float):
        """Returns quantile value of a pool"""
        pools = self._get_pools()
        if pool_id in pools:
            return calculate_quantile(
                    arr=pools[pool_id],
                    percentile=percentile
                )
        raise ValueError("pool_id not found.")

    def count_pool_items(self, pool_id: int) -> int:
        """Returns number of items in a pool"""
        pools = self._get_pools()
        if pool_id in pools:
            return len(self._get_pools()[pool_id])
        raise ValueError("pool_id not found.")
