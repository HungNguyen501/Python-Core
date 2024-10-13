"""APIs for pool data"""
from typing import List

from fastapi import APIRouter, Body, HTTPException, Depends
from src.pool_api.services import PoolService
from src.pool_api.dto import (
    PoolUpsertResponse,
    PoolStatisticsGetResponse,
)


router = APIRouter()


@router.post(path="/upsert", response_model=PoolUpsertResponse)
async def upsert_pool(
    pool_id: int = Body(),
    values: List[int] = Body(),
    pool_service: PoolService = Depends(),
):
    """Enpoint to append/insert a list into pool by pool_id
    Args:
        id(int): pool_id
        values(list): List of integer value
    Return status
    """
    status = pool_service.upsert_pool(
        pool_id=pool_id,
        values=values,
    )
    return PoolUpsertResponse(pool_id=pool_id, status=status)


@router.post("/statistics")
async def get_pool_statistics(
    pool_id: int = Body(),
    percentile: float = Body(),
    pool_service: PoolService = Depends(),
):
    """Endpoint to get statistics of a pool_id
    Args:
        pool_id(int): id of pool
        percentile(float): quantile in percentile form
    Return total number of elements in pool and its quantile value
    """
    try:
        return PoolStatisticsGetResponse(
            pool_id=pool_id,
            quantile_value=pool_service.calculate_quantile(
                pool_id=pool_id,
                percentile=percentile,
            ),
            total_count=pool_service.count_pool_items(
                pool_id=pool_id,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"{str(exc)}"
        ) from exc
