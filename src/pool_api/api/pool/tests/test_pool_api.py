"""Unit tests for module api"""
import sys

import pytest
from fastapi.testclient import TestClient
from src.pool_api.api.application import get_app


def make_test_client() -> TestClient:
    """Mock TestClient"""
    return TestClient(app=get_app())


def test_upsert_pool_with_appended():
    """Test endpoint /api/pool/upsert with inserted type"""
    response = make_test_client().post(
        url="/api/pool/upsert",
        json={
            "pool_id": 1,
            "values": [1, 2]
        }
    )
    assert response.status_code == 200
    assert response.json() == {"pool_id": 1, "status": "inserted"}


def test_upsert_pool_with_inserted(*_):
    """Test endpoint /api/pool/upsert with appended type"""
    response = make_test_client().post(
        url="/api/pool/upsert",
        json={
            "pool_id": 1,
            "values": [1, 2, 3]
        }
    )
    assert response.status_code == 200
    assert response.json() == {"pool_id": 1, "status": "appended"}


def test_get_pool_statistics(*_):
    """Test endpoint /api/pool/statistics"""
    response = make_test_client().post(
        url="/api/pool/statistics",
        json={
            "pool_id": 1,
            "percentile": 35
        }
    )
    assert response.status_code == 200
    assert response.json() == {"pool_id": 1, "quantile_value": 1, "total_count": 5}


def test_get_pool_statistics_with_value_error(*_):
    """Test endpoint /api/pool/statistics with percentile value error"""
    response = make_test_client().post(
        url="/api/pool/statistics",
        json={
            "pool_id": 1,
            "percentile": 130.5
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Percentile must be in range [0, 100]"
    }


def test_get_pool_statistics_with_id_not_found(*_):
    """Test endpoint /api/pool/statistics with pool_id not found"""
    response = make_test_client().post(
        url="/api/pool/statistics",
        json={
            "pool_id": 2,
            "percentile": 50
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "pool_id not found."}


if __name__ == "__main__":
    sys.exit(pytest.main([__file__] + sys.argv[1:]))
