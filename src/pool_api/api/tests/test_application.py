"""Unit tests for application module"""
from unittest.mock import patch, call
import sys

import pytest
from src.pool_api.api.application import get_app


@patch(target="src.pool_api.api.application.get_api_router")
@patch(target="src.pool_api.api.application.FastAPI")
def test_get_app(mock_fastapi, mock_get_api_router, *_):
    """Test get_app function"""
    mock_app = get_app()
    assert mock_fastapi.call_args == call(
        title="API service",
    )
    # pylint: disable=no-member
    assert mock_app.include_router.call_args == call(
        router=mock_get_api_router(),
        prefix="/api"
    )


if __name__ == "__main__":
    sys.exit(pytest.main([__file__] + sys.argv[1:]))
