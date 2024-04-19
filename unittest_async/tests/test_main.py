"""Unit tests for main module"""
from unittest.mock import patch, mock_open, call, MagicMock, AsyncMock

import pytest
from unittest_async.main import fetch_event, write_outputs, main


@pytest.mark.asyncio
@patch("unittest_async.main.asyncio.sleep")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="{\"1\": {\"data\": \"dummy\"}}"
)
async def test_fetch_event(*_):
    """Test fetch_event function"""
    id_1 = await fetch_event(session=MagicMock(), event_id="1")
    id_20 = await fetch_event(session=MagicMock(), event_id="-1")
    assert id_1 == {'data': 'dummy'}
    assert id_20 == {"-1": "event_id not found"}


@pytest.mark.asyncio
@patch("unittest_async.main.fetch_event", return_value={'data': 'dummy'})
@patch("unittest_async.main.aiofiles.open")
async def test_write_outputs(mock_aiofiles, *_):
    """Test function write_outputs"""
    mock_sem = AsyncMock()
    await write_outputs(
        output_file_path="./fk.json",
        session=MagicMock(),
        event_id="-1",
        semaphore_config=mock_sem,
    )
    assert mock_aiofiles.return_value.__aenter__\
        .return_value.write.call_args == call("{'data': 'dummy'}\n")


@pytest.mark.asyncio
@patch("unittest_async.main.write_outputs")
@patch("unittest_async.main.asyncio.gather", side_effect=AsyncMock())
@patch("unittest_async.main.subprocess.run")
async def test_main(mock_subprocess_run, mock_asyncio_gather, *_):
    """Test main function"""
    await main(
        output_file="zombie.dum",
        li_events=["-2", "-1", "0"],
    )
    assert mock_subprocess_run.call_args == call(args=['rm', '-rf', 'zombie.dum'], check=True)
    assert len(mock_asyncio_gather.call_args.args) == 3
