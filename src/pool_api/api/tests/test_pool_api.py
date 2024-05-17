"""Unit tests for module api"""
from functools import cache
from unittest.mock import patch
import sys

import pytest
from fastapi.testclient import TestClient
from src.pool_api.api.pool_api import app


@cache
def mock_test_client() -> TestClient:
    """Mock TestClient"""
    return TestClient(app=app)


def test_upsert_pool_with_appended():
    """Test endpoint /upsert with appended type"""
    response = mock_test_client().post(
        url="/upsert",
        json={
            "pool_id": 1,
            "values": [1, 2]
        }
    )
    assert response.status_code == 200
    assert response.json() == {"status": "inserted"}


@patch("src.pool_api.api.pool_api.pools", return_value={1: [1]})
def test_upsert_pool_with_inserted(*_):
    """Test endpoint /upsert with appended type"""
    response = mock_test_client().post(
        url="/upsert",
        json={
            "pool_id": 1,
            "values": [1, 2]
        }
    )
    assert response.status_code == 200
    assert response.json() == {"status": "appended"}


@patch("src.pool_api.api.pool_api.pools", {1: [1, 9, 4]})
def test_get_pool_statistics(*_):
    """Test endpoint /statistics"""
    response = mock_test_client().post(
        url="/statistics",
        json={
            "pool_id": 1,
            "percentile": 35
        }
    )
    assert response.status_code == 200
    assert response.json() == {"quantile_value": 4, "total count": 3}


@patch("src.pool_api.api.pool_api.pools", {1: [1, 9, 4]})
def test_get_pool_statistics_with_value_error(*_):
    """Test endpoint /statistics with percentile value error"""
    response = mock_test_client().post(
        url="/statistics",
        json={
            "pool_id": 1,
            "percentile": 130.5
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Percentile must be in range [0, 100]"
    }


@patch(
    "src.pool_api.api.pool_api.pools", {1: [1, 9, 4]})
def test_get_pool_statistics_with_id_not_found(*_):
    """Test endpoint /statistics with pool_id not found"""
    response = mock_test_client().post(
        url="/statistics",
        json={
            "pool_id": 2,
            "percentile": 50
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Not found pool_id"}


if __name__ == "__main__":
    sys.exit(pytest.main([__file__] + sys.argv[1:]))
