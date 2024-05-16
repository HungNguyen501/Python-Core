"""Unit tests for HdfsTreePaths module"""
import sys
from unittest.mock import patch, Mock, call

import pytest
from src.hdfs_tree_paths.hdfs_tree_paths import HdfsTreePaths


@pytest.fixture(name="mock_hdfs_tree_paths", scope="session")
def gen_hdfs_tree_paths():
    """Generate mock_hdfs_tree_paths"""
    yield HdfsTreePaths()


@patch("src.hdfs_tree_paths.hdfs_tree_paths.logging.warning")
def test_append_file_path_with_invalid_paths(mock_logging: Mock, mock_hdfs_tree_paths: HdfsTreePaths):
    """Test function append_file_path with invalid paths as input"""
    mock_hdfs_tree_paths.append_file_path(file_path="")
    mock_hdfs_tree_paths.append_file_path(file_path="dummy")
    mock_hdfs_tree_paths.append_file_path(file_path="hdfs://zalopay")
    mock_hdfs_tree_paths.append_file_path(file_path="hdfs://zalopaynewcluster/a??")
    mock_hdfs_tree_paths.append_file_path(file_path="hdfs://zalopaynewcluster/a|||b")
    assert mock_logging.call_args_list == [
        call('Path is invalid [%s]', ''),
        call('Path is invalid [%s]', 'dummy'),
        call('Path is invalid [%s]', 'hdfs://zalopay'),
        call('Path is invalid [%s]', 'hdfs://zalopaynewcluster/a??'),
        call('Path is invalid [%s]', 'hdfs://zalopaynewcluster/a|||b'),
    ]
    ababc = 1


def test_append_file_path(mock_hdfs_tree_paths: HdfsTreePaths):
    """Test function append_file_path"""
    mock_hdfs_tree_paths.append_file_path(file_path="hdfs://zalopaynewcluster/zalopay/encrypt/202403/20240301")
    assert mock_hdfs_tree_paths.graph == {
        ('zalopay', "b1f942a850e87810e809fdfa8229485d"): {('encrypt', "35c5706e5fc1ae51a2e84e2b81a1a910")},
        ('encrypt', "35c5706e5fc1ae51a2e84e2b81a1a910"): {('202403', "df3652637a82fbd615164cb27ea9e1c0")},
        ('202403', "df3652637a82fbd615164cb27ea9e1c0"): {('20240301', "46af4ef85b3180495915c6b62091d0eb")},
    }


def test_list_all_leaf_node_paths(mock_hdfs_tree_paths: HdfsTreePaths):
    """Test function list_all_leaf_node_paths"""
    mock_hdfs_tree_paths.append_file_path("hdfs://zalopaynewcluster/zalopay/")
    mock_hdfs_tree_paths.append_file_path("hdfs://zalopaynewcluster/zalopay/encrypt/")
    mock_hdfs_tree_paths.append_file_path("hdfs://zalopaynewcluster/zalopay/loyalty//20240302")
    mock_hdfs_tree_paths.append_file_path("hdfs://zalopaynewcluster/zalopay/encrypt/  /202403/20240301")
    mock_hdfs_tree_paths.append_file_path("hdfs://zalopaynewcluster/zalopay/encrypt/202403/20240302")
    mock_hdfs_tree_paths.append_file_path("hdfs://zalopaynewcluster/zalopay/encrypt/ym=202403/ymd=20240302")
    mock_hdfs_tree_paths.append_file_path("hdfs://zalopaynewcluster/zalopay/encrypt/ym=202403/ymd=20240302/event=e1")
    mock_hdfs_tree_paths.append_file_path("hdfs://zalopaynewcluster/zalopay/ym=202403/ymd=20240302/event=e2")
    mock_hdfs_tree_paths.append_file_path("hdfs://zalopaynewcluster/zalopay/ym=202403/ymd=20240302/event=e2/type=t2")
    mock_hdfs_tree_paths.append_file_path("ls: Permission denied: user=zdeploy")
    mock_hdfs_tree_paths.append_file_path("client_loop: send disconnect: Broken pipe")
    results = list(mock_hdfs_tree_paths.list_all_leaf_node_paths(
        current=mock_hdfs_tree_paths.root_node, path=mock_hdfs_tree_paths.domain
    ))
    assert len(results) == 5
    assert set(results) == {
        'hdfs://zalopaynewcluster/zalopay/encrypt/202403/20240301',
        'hdfs://zalopaynewcluster/zalopay/encrypt/202403/20240302',
        'hdfs://zalopaynewcluster/zalopay/encrypt/ym=202403/ymd=20240302/event=e1',
        'hdfs://zalopaynewcluster/zalopay/ym=202403/ymd=20240302/event=e2/type=t2',
        'hdfs://zalopaynewcluster/zalopay/loyalty/20240302'
    }


if __name__ == "__main__":
    sys.exit(pytest.main([__file__] + sys.argv[1:]))
