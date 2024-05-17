"""APIs for pool data"""
from typing import List

from fastapi import FastAPI, Body, HTTPException
from src.common.calculate_quantile.calculate_quantile import calculate_quantile

app = FastAPI()
pools = {}


@app.post("/upsert")
async def upsert_pool(pool_id: int = Body(), values: List[int] = Body()):
    """Enpoint to append/insert a list into pool by pool_id
    Args:
        id(int): pool_id
        values(list): List of integer value
    Return status
    """
    if pool := pools.get(pool_id):
        pool.extend(values)
        return {"status": "appended"}
    pools[pool_id] = values
    return {"status": "inserted"}


@app.post("/statistics")
async def get_pool_statistics(
    pool_id: int = Body(),
    percentile: float = Body()
):
    """Endpoint to get statistics of a pool_id
    Args:
        pool_id(int): id of pool
        percentile(float): quantile in percentile form
    Return total number of elements in pool and its quantile value
    """
    if pool := pools.get(pool_id):
        try:
            return {
                "quantile_value": calculate_quantile(
                    arr=pool,
                    percentile=percentile
                ),
                "total count": len(pool),
            }
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=f"{str(exc)}"
            ) from exc
    raise HTTPException(
        status_code=400,
        detail="Not found pool_id"
    )
