"""Crawler Engine Module"""
import asyncio
from datetime import datetime, timedelta
from typing import List, Any

from aiohttp import ClientSession


async def fetch_data(
    session: ClientSession, url: str,
    event_date: datetime, list_records: List[str],
    transform_data: Any
):
    """
        Consume data from URL and process this raw data
    """
    resp = await session.request(
        method="GET",
        url=url,
    )
    resp.raise_for_status()
    data = await resp.text()
    transform_data(data=data, list_records=list_records, event_date=event_date)


async def crawl_url(start_date: datetime, end_date: datetime, format_url: Any, transform_data: Any) -> List[List[str]]:
    """
        Crawl data in multiple days asynchronously
    """
    list_records = []
    async with ClientSession() as session:
        tasks = []
        target_date = start_date
        while target_date <= end_date:
            tasks.append(
                fetch_data(
                    session=session,
                    url=format_url(event_date=target_date),
                    event_date=target_date,
                    list_records=list_records,
                    transform_data=transform_data,
                )
            )
            target_date += timedelta(days=1)
        await asyncio.gather(*tasks)
    return list_records
