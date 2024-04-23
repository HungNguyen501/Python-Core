# """Unit tests for datahub module"""
# from unittest.mock import patch, AsyncMock, MagicMock, call

# import pytest
# from data_hub.datahub import (
#     search_datasets,
#     extract_dataset_info,
#     check_hdfs_path_exists,
#     verify_entity,
#     get_list_invalid_hdfs_datasets,
#     remove_datasets,
#     fetch_schema
# )


# @patch("data_hub.datahub.DataHubGraph")
# def test_search_datasets(*_):
#     """Test search_datasets function"""
#     mock_graph = MagicMock()
#     mock_graph.execute_graphql.return_value = {"search": {"total": 10, "searchResults": "monkey"}}
#     assert list(search_datasets(graph=mock_graph, search_pattern="dummy")) == ["monkey"]


# def test_extract_dataset_info():
#     """Test extract_dataset_info function"""
#     test_sample1 = [
#         {"entity": {
#             "properties": {"customProperties": [
#                            {"key": "database", "value": "hdfs_cluster_61"},
#                            {"key": "location", "value": "fake_location"},
#                            ]},
#             "deprecation": None,
#             "urn": "fake_urn",
#         }},
#         {"entity": {}},
#         {"entity": {"properties": {"customProperties": None}}},
#         {"entity": {"properties": {"customProperties": [{"key": "database", "value": "foo"}]}}},
#     ]
#     test_sample2 = [
#         {"entity": {
#             "properties": {"customProperties": [{"key": "dum", "value": "foo"}]},
#         }}
#     ]
#     assert extract_dataset_info(li_datasets=test_sample1) == [
#         {"database": "hdfs_cluster_61", "deprecation": None,
#          "location": "fake_location", "urn": "fake_urn"}]
#     assert extract_dataset_info(li_datasets=test_sample2) == []  # Catch KeyError Exception


# @pytest.mark.asyncio
# @patch("data_hub.datahub.asyncio.create_subprocess_shell", side_effect=AsyncMock())
# async def test_check_hdfs_path_exists(mock_create_subprocess_shell):
#     """Test check_hdfs_path_exists function"""
#     _ = await check_hdfs_path_exists(path="/animal/cat/")
#     assert mock_create_subprocess_shell.mock_calls == [
#         call('hdfs dfs -conf /home/hungnd8/hdfs_configs/zalopaynewcluster/hdfs-site.xml -test -d /animal/cat/')
#     ]


# @pytest.mark.asyncio
# @patch("data_hub.datahub.check_hdfs_path_exists", side_effect=[True, False])
# async def test_verify_entity(*_):
#     """Test verify_entity function"""
#     mock_semaphore_config = AsyncMock()
#     test_sample1 = {"deprecation": {"deprecated": True}, "urn": "tmp.fk"}
#     test_sample2 = {"location": "/dum/foo/", "urn": "tmp.fk"}
#     li_test = []
#     assert await verify_entity(entity=test_sample1, li_invalids=[], semaphore_config=mock_semaphore_config) is None
#     assert await verify_entity(entity=test_sample2, li_invalids=[], semaphore_config=mock_semaphore_config) is None
#     await verify_entity(entity=test_sample2, li_invalids=li_test, semaphore_config=mock_semaphore_config)
#     assert li_test == ["tmp.fk"]


# @pytest.mark.asyncio
# @patch("data_hub.datahub.verify_entity")
# @patch("data_hub.datahub.asyncio.gather", side_effect=AsyncMock())
# @patch("data_hub.datahub.asyncio.Semaphore")
# async def test_get_list_invalid_hdfs_datasets(mock_semaphore, mock_gather, *_):
#     """Test get_list_invalid_hdfs_datasets function"""
#     await get_list_invalid_hdfs_datasets([-1, -1], [])
#     assert mock_semaphore.mock_calls == [call(value=50)]
#     assert len(mock_gather.call_args) == 2


# def test_remove_datasets():
#     """Test remove_datasets function"""
#     mock_graph = MagicMock()
#     remove_datasets(mock_graph, [-1, -1])
#     assert mock_graph.mock_calls == [call.delete_entity(urn=-1, hard=False),
#                                      call.delete_entity(urn=-1, hard=False)]


# def test_fetch_schema():
#     """Test fetch_schema function"""
#     mock_graph = MagicMock()
#     fetch_schema(mock_graph, "fake")
#     assert mock_graph.mock_calls
