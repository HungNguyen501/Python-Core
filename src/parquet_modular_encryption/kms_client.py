"""Implement AwsKmsClient module"""
import base64
import logging

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import pyarrow.parquet.encryption as pe


class AwsKmsClient(pe.KmsClient):
    """Implement AwsKmsClient to wrap/ unwrap key (data) by exchanging keys with Aws Kms Server"""
    def __init__(self, kms_connection_config,):
        """Initial AwsKms object"""
        pe.KmsClient.__init__(self)
        if proxies_https := kms_connection_config.custom_kms_conf["proxies_https"]:
            config = Config(proxies={"https": proxies_https})
        else:
            config = None
        self.kms_client = boto3.client(
            "kms",
            config=config,
            region_name=kms_connection_config.custom_kms_conf["region_name"],
            aws_access_key_id=kms_connection_config.custom_kms_conf["aws_access_key_id"],
            aws_secret_access_key=kms_connection_config.custom_kms_conf["aws_secret_access_key"],
        )

    def wrap_key(self, key_bytes: bytes, master_key_identifier: str,) -> bytes:
        """Wrap key by master key specified by master_key_identifier"""
        try:
            wrapped_key = self.kms_client.encrypt(
                    KeyId=f"alias/{master_key_identifier}",
                    Plaintext=key_bytes,
                )["CiphertextBlob"]
            return base64.b64encode(wrapped_key)
        except ClientError as err:
            logging.error("Couldn't encrypt text. Here's why: %s",
                          err.response["Error"]["Message"],)
            return None

    def unwrap_key(self, wrapped_key: bytes, master_key_identifier: str,) -> bytes:
        """Unwrap key by master key specified by master_key_identifier"""
        try:
            decoded_wrapped_key = base64.b64decode(wrapped_key)
            return self.kms_client.decrypt(
                KeyId=f"alias/{master_key_identifier}",
                CiphertextBlob=decoded_wrapped_key
            )["Plaintext"]
        except ClientError as err:
            logging.error("Couldn't decrypt your ciphertext. Here's why: %s",
                          err.response["Error"]["Message"],)
            return None
