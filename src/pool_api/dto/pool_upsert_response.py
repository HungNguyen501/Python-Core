"""Response for get_pool_statistics"""
from pydantic import BaseModel


class PoolUpsertResponse(BaseModel):
    """Pool Upsert Response"""
    pool_id: int
    status: str
