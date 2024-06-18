"""Unit tests for crawler engine module"""
from datetime import datetime
from unittest.mock import patch, call, MagicMock, AsyncMock

import pytest
from src.web_crawler.crawler_engine import fetch_data, crawl_url


@pytest.mark.asyncio
async def test_fetch_data():
    """Test fetch_data function"""
    mock_client_session = AsyncMock()
    mock_transform_data = MagicMock()
    await fetch_data(
        session=mock_client_session,
        url="https://fake_url",
        event_date=datetime(year=1990, month=12, day=31),
        list_records=["foo1", "foo2"],
        transform_data=mock_transform_data,
    )
    assert mock_client_session \
        .request.call_args_list == [call(method="GET", url="https://fake_url")]


@pytest.mark.asyncio
@patch("src.unittest_async.main.asyncio.gather", side_effect=AsyncMock())
async def test_crawl_url(mock_gather, *_):
    """Test crawl_url function"""
    start_date = datetime(year=1990, month=12, day=1)
    end_date = datetime(year=1990, month=12, day=31)
    await crawl_url(
        start_date=start_date,
        end_date=end_date,
        format_url=MagicMock(),
        transform_data=MagicMock(),
    )
    assert len(mock_gather.call_args.args) == (end_date - start_date).days + 1
