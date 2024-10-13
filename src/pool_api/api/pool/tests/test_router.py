"""Test router module"""
from unittest.mock import patch, call

from src.pool_api.api.pool.router import get_api_router


@patch(target="src.pool_api.api.pool.pool_api")
@patch(target="src.pool_api.api.pool.router.APIRouter")
def test_get_api_router(mock_api_router, *_):
    """Test get_api_router function"""
    _ = get_api_router()
    assert mock_api_router.call_args == call(prefix="/pool")
