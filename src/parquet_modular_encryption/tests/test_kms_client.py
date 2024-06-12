"""Unit tests for AwsKmsClient module"""
from unittest.mock import patch, call, MagicMock

import pytest
from botocore.exceptions import ClientError
from src.parquet_modular_encryption.kms_client import AwsKmsClient


@pytest.fixture(name="mock_kms_connection_config", scope="session")
def gen_mock_kms_connection_config():
    """Create mock_kms_connection_config"""
    mock_kms_connection_config = MagicMock()
    mock_data = {
        "proxies_https": None,
        "region_name": "us",
        "aws_access_key_id": "fake_id",
        "aws_secret_access_key": "dump_key",
    }
    mock_kms_connection_config.custom_kms_conf.__getitem__.side_effect = mock_data.__getitem__
    return mock_kms_connection_config


@patch("src.parquet_modular_encryption.kms_client.pe.KmsClient")
@patch("src.parquet_modular_encryption.kms_client.boto3.client")
def test_wrap_key(mock_boto3_client: MagicMock, _, mock_kms_connection_config):
    """Test wrap_key function"""
    mock_boto3_client.return_value.encrypt.return_value = {"CiphertextBlob": b"cipher_data"}
    mock_aws_kms_client = AwsKmsClient(kms_connection_config=mock_kms_connection_config)
    cipher_text = mock_aws_kms_client.wrap_key(key_bytes=b"treasure", master_key_identifier="data_key")
    assert mock_boto3_client.return_value.encrypt.call_args_list == [
        call(KeyId='alias/data_key', Plaintext=b'treasure')]
    assert cipher_text == b'Y2lwaGVyX2RhdGE='


@patch("src.parquet_modular_encryption.kms_client.pe.KmsClient")
@patch("src.parquet_modular_encryption.kms_client.boto3.client")
def test_wrap_key_with_exception(mock_boto3_client: MagicMock, _, mock_kms_connection_config):
    """Test wrap_key function with ClientError"""
    mock_boto3_client.return_value.encrypt.side_effect = ClientError({"Error": {"Message": ""}}, "")
    mock_aws_kms_client = AwsKmsClient(kms_connection_config=mock_kms_connection_config())
    assert mock_aws_kms_client.wrap_key(key_bytes=b"treasure", master_key_identifier="data_key") is None


@patch("src.parquet_modular_encryption.kms_client.pe.KmsClient")
@patch("src.parquet_modular_encryption.kms_client.boto3.client")
def test_unwrap_key(mock_boto3_client: MagicMock, _, mock_kms_connection_config):
    """Test unwrap_key function"""
    mock_boto3_client.return_value.decrypt.return_value = {"Plaintext": b"plain_text"}
    mock_aws_kms_client = AwsKmsClient(kms_connection_config=mock_kms_connection_config)
    plain_text = mock_aws_kms_client.unwrap_key(wrapped_key=b'Y2lwaGVyX2RhdGE=', master_key_identifier="data_key")
    assert mock_boto3_client.return_value.decrypt.call_args_list == [
        call(KeyId='alias/data_key', CiphertextBlob=b'cipher_data')]
    assert plain_text == b"plain_text"


@patch("src.parquet_modular_encryption.kms_client.pe.KmsClient")
@patch("src.parquet_modular_encryption.kms_client.boto3.client")
def test_unwrap_key_with_exception(mock_boto3_client: MagicMock, _, mock_kms_connection_config):
    """Test unwrap_key function with ClientError"""
    mock_boto3_client.return_value.decrypt.side_effect = ClientError({"Error": {"Message": ""}}, "")
    mock_aws_kms_client = AwsKmsClient(kms_connection_config=mock_kms_connection_config())
    assert mock_aws_kms_client.unwrap_key(wrapped_key=b'Y2lwaGVyX2RhdGE=', master_key_identifier="data_key") is None
