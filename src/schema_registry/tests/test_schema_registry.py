"""Unit tests for Schema Registry"""
from unittest.mock import patch, call, MagicMock

import pytest
from src.schema_registry.schema_registry import SchemaRegistry


@pytest.fixture(name="mock_schema_registry", scope="session")
def gen_mock_schema_registry():
    yield SchemaRegistry(url="http://local", token="fake")


@patch("src.schema_registry.schema_registry.requests")
def test_func_list_subjects(mock_requests: MagicMock, mock_schema_registry):
    """Test list_subjects function"""
    mock_requests.get.return_value.json.return_value = ["subject3", "subject1", "subject2"]
    assert mock_schema_registry.list_subjects() == ["subject1", "subject2", "subject3"]
    assert mock_requests.get.call_args_list == [call(
        url='http://local/subjects',
        headers={
            'Authorization': 'Basic fake',
            'Accept': 'application/vnd.schemaregistry.v1+json, application/vnd.schemaregistry+json, application/json'
        },
        timeout=10)]


@patch("src.schema_registry.schema_registry.requests")
def test_func_list_subject_versions(mock_requests: MagicMock, mock_schema_registry):
    """Test list_subject_versions function"""
    mock_requests.get.return_value.json.return_value = [1, 2, 3, 4]
    assert mock_schema_registry.list_subject_versions(subject="dum") == [1, 2, 3, 4]
    assert mock_requests.get.call_args_list == [call(
        url='http://local/subjects/dum/versions',
        headers={
            'Authorization': 'Basic fake',
            'Accept': 'application/vnd.schemaregistry.v1+json, application/vnd.schemaregistry+json, application/json'
        },
        timeout=10)]


@patch("src.schema_registry.schema_registry.requests")
def test_func_get_subject(mock_requests: MagicMock, mock_schema_registry):
    """Test get_subject function"""
    mock_requests.get.return_value.json.return_value = {
        "name": "test",
        "version": 1,
        "schemaType": "PROTOBUF",
        "schema": "{\"type\": \"string\"}",
    }
    assert mock_schema_registry.get_subject(subject="dum") == {
        "name": "test",
        "version": 1,
        "schemaType": "PROTOBUF",
        "schema": "{\"type\": \"string\"}",
    }
    assert mock_requests.get.call_args_list == [call(
        url='http://local/subjects/dum/versions/latest',
        headers={
            'Authorization': 'Basic fake',
            'Accept': 'application/vnd.schemaregistry.v1+json, application/vnd.schemaregistry+json, application/json'
        },
        timeout=10)]


@patch("src.schema_registry.schema_registry.requests")
def test_func_delete_subject(mock_requests: MagicMock, mock_schema_registry):
    """Test delete_subject function"""
    mock_schema_registry.delete_subject(subject="dum")
    assert mock_requests.delete.call_args_list == [call(
        url='http://local/subjects/dum?permanent=false',
        timeout=10)]


@patch("src.schema_registry.schema_registry.requests")
def test_func_delete_subject_version(mock_requests: MagicMock, mock_schema_registry):
    """Test delete_subject_version function"""
    mock_schema_registry.delete_subject_version(subject="dum", version_id=-1, is_permanent="true")
    assert mock_requests.delete.call_args_list == [call(
        url='http://local/subjects/dum/versions/-1?permanent=true',
        timeout=10)]
