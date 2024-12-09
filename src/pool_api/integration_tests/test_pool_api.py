"""Integration test for pool_api"""
import os

import httpx
import pytest
from faker import Faker


fake = Faker()


@pytest.mark.skipif(os.getenv("INTEGRATION_TEST") != "ENABLE", reason="Only run tests when enabling integration_tests")
@pytest.fixture(name="client", scope="session")
def gen_client():
    """Generate mock_hdfs_tree_paths"""
    with httpx.Client() as client:
        yield client


@pytest.mark.skipif(os.getenv("INTEGRATION_TEST") != "ENABLE", reason="Only run tests when enabling integration_tests")
def test_upsert_pool(client):
    """Test /upsert api"""
    random_pool_id = fake.random_number()
    insert_resp = client.post(
        url="http://localhost:8501/api/pool/upsert",
        json={
            "pool_id": random_pool_id,
            "values": list(range(5))
        }
    )
    assert insert_resp.status_code == 200
    assert insert_resp.text == '{"pool_id": {pool_id}, "status":"inserted"}'.format(pool_id=random_pool_id)
    append_resp = client.post(
        url="http://localhost:8501/api/pool/upsert",
        json={
            "pool_id": random_pool_id,
            "values": list(range(5))
        }
    )
    assert append_resp.status_code == 200
    assert append_resp.text == '{"pool_id": {pool_id}, "status":"appended"}'.format(pool_id=random_pool_id)


@pytest.mark.skipif(not os.getenv("INTEGRATION_TEST"), reason="Only run tests when enabling integration_tests")
def test_get_statistics(client):
    """Test /statistics api"""
    random_pool_id = fake.random_number()
    not_found_resp = client.post(
        url="http://localhost:8501/api/pool/statistics",
        json={
            "pool_id": fake.random_number(),
            "percentile": 50.9
        }
    )
    assert not_found_resp.status_code == 400
    assert not_found_resp.text == '{"detail":"pool_id not found."}'

    insert_resp = client.post(
        url="http://localhost:8501/api/pool/upsert",
        json={
            "pool_id": random_pool_id,
            "values": list(range(10))
        }
    )
    assert insert_resp.status_code == 200
    assert insert_resp.text == '{"pool_id": {pool_id}, "status":"inserted"}'.format(pool_id=random_pool_id)

    statistics_resp = client.post(
        url="http://localhost:8501/api/pool/statistics",
        json={
            "pool_id": random_pool_id,
            "percentile": 50.9
        }
    )
    assert statistics_resp.status_code == 200
    assert statistics_resp.json() == {'quantile_value': 5, 'total_count': 10}
