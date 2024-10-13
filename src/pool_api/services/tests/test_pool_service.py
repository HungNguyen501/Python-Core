"""Test PoolService module"""
import pytest
from src.pool_api.repositories import DataManager
from src.pool_api.services import PoolService


def test_pool_service():
    """Test PoolService class"""
    pool_service = PoolService(db=DataManager())
    assert pool_service.upsert_pool(pool_id=10, values=[0, 1, 2]) == "inserted"
    assert pool_service.upsert_pool(pool_id=10, values=[1, 2, 3]) == "appended"
    assert pool_service.calculate_quantile(pool_id=10, percentile=90) == 3
    assert pool_service.count_pool_items(pool_id=10) == 6
    with pytest.raises(ValueError):
        pool_service.calculate_quantile(pool_id=-1, percentile=22)
    with pytest.raises(ValueError):
        pool_service.count_pool_items(pool_id=-1)
