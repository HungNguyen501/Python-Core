"""Implement Parquet Modular Encryption module"""
from datetime import timedelta
from typing import Any
import os
import subprocess

from pyarrow import Table
from pyarrow.fs import FileSystem, HadoopFileSystem
import pyarrow.parquet as pq
import pyarrow.parquet.encryption as pe
from src.parquet_modular_encryption.kms_client import AwsKmsClient


def connect_to_hdfs(host: str, port: int, extra_conf: dict) -> HadoopFileSystem:
    """Connect to HDFS

    Args:
        host(str): HDFS hostname
        port(int): HDFS port, port = 0 if using HA

    Returns HadoopFileSystem object to access HDFS
    """
    # Export ARROW_LIBHDFS_DIR var
    with subprocess.Popen(
        args="locate -l 1 libhdfs.so",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy(),
        shell=True,
    ) as process:
        stdout, stderr = process.communicate()
        if stderr:
            raise RuntimeError("Failed to get libhdfs path")
        libhdfsso_path = stdout.decode("utf-8").rstrip()
        os.environ["ARROW_LIBHDFS_DIR"] = os.path.dirname(libhdfsso_path)
    # Export CLASSPATH var
    with subprocess.Popen(
        args="/usr/bin/hdfs classpath --glob",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy(),
        shell=True,
    ) as process:
        stdout, stderr = process.communicate()
        if stderr:
            raise RuntimeError("Failed to get hdfs classpath")
        hadoop_cp = stdout.decode("utf-8").rstrip()
        os.environ["ARROW_LIBHDFS_DIR"] = os.path.dirname(libhdfsso_path)
        if "CLASSPATH" in os.environ:
            os.environ["CLASSPATH"] = os.environ["CLASSPATH"] + ":" + hadoop_cp
        else:
            os.environ["CLASSPATH"] = hadoop_cp
    return HadoopFileSystem(host, port, extra_conf=extra_conf)


def kms_factory(kms_connection_config):
    """Returns AwsKmsClient object"""
    return AwsKmsClient(kms_connection_config)


def encrypt_to_parquet_file(location: str, table: Table, file_encryption_properties: Any, fs: FileSystem = None):
    """Encrypt data to parquet file"""
    with pq.ParquetWriter(
        where=location,
        schema=table.schema,
        filesystem=fs,
        encryption_properties=file_encryption_properties,
    ) as writer:
        writer.write_table(table)


def decrypt_parquet_file(
    location: str, crypto_factory: Any,
    kms_connection_config: Any, fs: FileSystem = None
) -> Table:
    """Decrypt data of parquet file"""
    decryption_config = pe.DecryptionConfiguration(cache_lifetime=timedelta(minutes=10.0))
    file_decryption_properties = crypto_factory.file_decryption_properties(
        kms_connection_config,
        decryption_config,
    )
    return pq.ParquetFile(
        source=location,
        filesystem=fs,
        decryption_properties=file_decryption_properties,
    ).read()
