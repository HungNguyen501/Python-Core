"""Test data_manager module"""
from src.pool_api.repositories import (
    DataManager,
    PoolEntity,
    generate_pools,
)


def test_data_manager():
    """Test DataManager class"""
    data_manager_instance = DataManager()
    assert isinstance(data_manager_instance.pool_entity, PoolEntity)
    assert isinstance(data_manager_instance.get_pools(), dict)


def test_generate_pools():
    """Test generate_pools function"""
    assert generate_pools().get_pools is not None
