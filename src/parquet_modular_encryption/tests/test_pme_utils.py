"""Unit test for Parquet Modular Encryption module"""
from unittest.mock import patch, call, MagicMock
from datetime import timedelta

import pytest
from src.parquet_modular_encryption.pme_utils import (
    connect_to_hdfs,
    kms_factory,
    encrypt_to_parquet_file,
    decrypt_parquet_file,
)


@patch("src.parquet_modular_encryption.pme_utils.HadoopFileSystem")
@patch("src.parquet_modular_encryption.pme_utils.os")
@patch("src.parquet_modular_encryption.pme_utils.subprocess")
def test_connect_to_hdfs(mock_subprocess: MagicMock, mock_os: MagicMock, mock_hadoop_fs: MagicMock,):
    """Test connect_to_hdfs function"""
    mock_subprocess.Popen.return_value \
        .__enter__.return_value.communicate.side_effect = [
            (b"path/to/libhdfsso/libhdfs.so", None), (b"path/to/classpath/classpath.jar", None),
            (b"", None), (b"/path/to/CLASSPATH", None),
        ]
    mock_os.path.dirname.side_effect = [
        "path/to/libhdfsso", "path/to/classpath",
        "", ""]
    mock_os.environ.__contains__.side_effect = [False, True]
    mock_os.environ.__getitem__.side_effect = [False, True]
    # Scenario env vars don't have CLASSPATH yet
    connect_to_hdfs(host="local/", port=-1, extra_conf={})
    assert mock_os.environ.__setitem__.call_args_list == [
        call('ARROW_LIBHDFS_DIR', 'path/to/libhdfsso'),
        call('ARROW_LIBHDFS_DIR', 'path/to/classpath'),
        call('CLASSPATH', 'path/to/classpath/classpath.jar'),]
    assert mock_hadoop_fs.call_args_list == [call('local/', -1, extra_conf={})]
    # Scenario env vars have CLASSPATH already
    mock_os_envs = {"CLASSPATH": "/root_path"}
    mock_os.environ.__getitem__.side_effect = mock_os_envs.__getitem__
    mock_os.environ.__setitem__.side_effect = mock_os_envs.__setitem__
    connect_to_hdfs(host="local/", port=-1, extra_conf={})
    assert mock_os.environ["CLASSPATH"] == "/root_path:/path/to/CLASSPATH"


@patch("src.parquet_modular_encryption.pme_utils.os")
@patch("src.parquet_modular_encryption.pme_utils.subprocess")
def test_connect_to_hdfs_with_exceptions(mock_subprocess: MagicMock, mock_os):
    """
        Test connect_to_hdfs function in case it raises exception
        when checking libhdfs and hdfs classpath modules in command line
    """
    mock_os.path.dirname.return_value = ""
    mock_subprocess.Popen.return_value \
        .__enter__.return_value.communicate.side_effect = [
            (b"", "error"),  # Scenario 1
            (b"", None),  # Scenario 2
            (b"", "error"),
        ]
    with pytest.raises(RuntimeError) as exc1:
        connect_to_hdfs(host="local/", port=-1, extra_conf={})
    assert exc1.value.args == ('Failed to get libhdfs path',)
    with pytest.raises(RuntimeError) as exc2:
        connect_to_hdfs(host="local/", port=-1, extra_conf={})
    assert exc2.value.args == ("Failed to get hdfs classpath",)


@patch("src.parquet_modular_encryption.kms_client.pe.KmsConnectionConfig")
@patch("src.parquet_modular_encryption.kms_client.boto3.client")
def test_kms_factory(mock_boto3_client: MagicMock, mock_kms_config, *_):
    """Test kms_factory function"""
    kms_factory(mock_kms_config)
    assert mock_boto3_client.called is True


@patch("src.parquet_modular_encryption.pme_utils.Table")
@patch("src.parquet_modular_encryption.pme_utils.pq.ParquetWriter")
def test_encrypt_to_parquet_file(mock_parquet_writer: MagicMock, mock_table: MagicMock):
    """Test encrypt_to_parquet_file function"""
    mock_table.schema = "foo_schema"
    encrypt_to_parquet_file(location="/temp/", table=mock_table, file_encryption_properties=None, fs=None)
    assert mock_parquet_writer.call_args_list == [
        call(where='/temp/', schema="foo_schema", filesystem=None, encryption_properties=None)
    ]
    assert mock_parquet_writer.return_value.__enter__ \
        .return_value.write_table.called is True


@patch("src.parquet_modular_encryption.pme_utils.pe.DecryptionConfiguration")
@patch("src.parquet_modular_encryption.pme_utils.pq.ParquetFile")
def test_decrypt_parquet_file(mock_parquet_file: MagicMock, mock_decrypt_config: MagicMock):
    """Test decrypt_parquet_file function"""
    mock_kms_config = MagicMock()
    mock_crypto_factory = MagicMock()
    mock_crypto_factory.file_decryption_properties.return_value = "foo"
    decrypt_parquet_file(
        location="/temp/",
        kms_connection_config=mock_kms_config,
        crypto_factory=mock_crypto_factory,)
    assert mock_decrypt_config.call_args_list == [
        call(cache_lifetime=timedelta(seconds=600))]
    assert mock_parquet_file.call_args_list == [
        call(source='/temp/', filesystem=None, decryption_properties="foo")]
    assert mock_parquet_file.return_value.read.called is True
