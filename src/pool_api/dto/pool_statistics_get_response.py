"""Response for get_pool_statistics"""
from pydantic import BaseModel


class PoolStatisticsGetResponse(BaseModel):
    """Pool Statistics Get Response"""
    pool_id: int
    quantile_value: int
    total_count: int
