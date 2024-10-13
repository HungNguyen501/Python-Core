"""Test pool_api"""
import httpx
import pytest
from faker import Faker


fake = Faker()


@pytest.fixture(name="client", scope="session")
def gen_client():
    """Generate mock_hdfs_tree_paths"""
    with httpx.Client() as client:
        yield client


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
    assert insert_resp.text == '{"status":"inserted"}'
    
    append_resp = client.post(
        url="http://localhost:8501/api/pool/upsert",
        json={
            "pool_id": random_pool_id,
            "values": list(range(5))
        }
    )
    assert append_resp.status_code == 200
    assert append_resp.text == '{"status":"appended"}'


def test_get_statistics(client):
    """Test /statistics api"""
    random_pool_id = fake.random_number()
    insert_resp = client.post(
        url="http://localhost:8501/api/pool/upsert",
        json={
            "pool_id": random_pool_id,
            "values": list(range(10))
        }
    )
    assert insert_resp.status_code == 200
    assert insert_resp.text == '{"status":"inserted"}'

    statistics_resp = client.post(
        url="http://localhost:8501/api/pool/statistics",
        json={
            "pool_id": random_pool_id,
            "percentile": 50.9
        }
    )
    assert statistics_resp.status_code == 200
    assert statistics_resp.json() == {'quantile_value': 5, 'total_count': 10}

    not_found_resp = client.post(
        url="http://localhost:8501/api/pool/statistics",
        json={
            "pool_id": random_pool_id,
            "percentile": 50.9
        }
    )
    