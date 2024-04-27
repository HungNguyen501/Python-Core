"""Schema Registry"""
from typing import List, Dict
import requests


class SchemaRegistry:
    """SchemaRegistry Model"""
    def __init__(self, url: str, token: str):
        """Init Schema Registry

        Args:
            url(str): url of schema registry api
            token(str): token for schema registry authorization
        """
        self.host = url
        self.headers = {
            "Authorization": f"Basic {token}",
            "Accept": "application/vnd.schemaregistry.v1+json, application/vnd.schemaregistry+json, application/json",
        }

    def list_subjects(self) -> List[str]:
        """List all names of subjects"""
        resp = requests.get(
            url=f"{self.host}/subjects",
            headers=self.headers,
            timeout=10,)
        resp.raise_for_status()
        return sorted(resp.json())

    def list_subject_versions(self, subject: str) -> List[int]:
        """List all versions of a subject

        Args:
            subject(str): name of subject

        Returns versions of the subject
        """
        resp = requests.get(
            url=f"{self.host}/subjects/{subject}/versions",
            headers=self.headers,
            timeout=10,)
        resp.raise_for_status()
        return resp.json()

    def get_subject(self, subject: str, version_id: int = -1) -> Dict:
        """Fecth content of a subject based on version_id

        Args:
            subject(str): subject name
            version_id(int): version

        Returns content of subject
        """
        version_id = "latest" if version_id == -1 else version_id
        resp = requests.get(
            url=f"{self.host}/subjects/{subject}/versions/{version_id}",
            headers=self.headers,
            timeout=10,)
        resp.raise_for_status()
        return resp.json()

    def delete_subject(self, subject: str, is_permanent: str = "false"):
        """Delete all versions of a subject

        subject(str): subject name
        is_permenant(boolean): hard-delete if true else soft-delete
        """
        resp = requests.delete(
            url=f"{self.host}/subjects/{subject}?permanent={is_permanent}",
            timeout=10,)
        resp.raise_for_status()

    def delete_subject_version(self, subject: str, version_id: int, is_permanent: str = "false"):
        """Delete specific version of a subject

        subject(str): subject name
        is_permenant(boolean): hard-delete if true else soft-delete
        """
        resp = requests.delete(
            url=f"{self.host}/subjects/{subject}/versions/{version_id}?permanent={is_permanent}",
            timeout=10,)
        resp.raise_for_status()
