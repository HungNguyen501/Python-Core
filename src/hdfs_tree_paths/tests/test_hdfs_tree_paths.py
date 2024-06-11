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
    mock_hdfs_tree_paths.append_file_path(file_path="hdfs://lake")
    mock_hdfs_tree_paths.append_file_path(file_path="hdfs://hdfs_cluster/a??")
    mock_hdfs_tree_paths.append_file_path(file_path="hdfs://hdfs_cluster/a|||b")
    assert mock_logging.call_args_list == [
        call('Path is invalid [%s]', ''),
        call('Path is invalid [%s]', 'dummy'),
        call('Path is invalid [%s]', 'hdfs://lake'),
        call('Path is invalid [%s]', 'hdfs://hdfs_cluster/a??'),
        call('Path is invalid [%s]', 'hdfs://hdfs_cluster/a|||b'),
    ]


def test_append_file_path(mock_hdfs_tree_paths: HdfsTreePaths):
    """Test function append_file_path"""
    mock_hdfs_tree_paths.append_file_path(file_path="hdfs://hdfs_cluster/lake/encrypt/202403/20240301")
    assert mock_hdfs_tree_paths.graph == {
        ('lake', '97d986e2afa2c72986972e6433fbeaf9'): {('encrypt', 'e63354f46dce52bcba42e3d21711afe8')},
        ('encrypt', 'e63354f46dce52bcba42e3d21711afe8'): {('202403', 'eac68ba120e7ebcb528abefed8acbdc6')},
        ('202403', 'eac68ba120e7ebcb528abefed8acbdc6'): {('20240301', '176c73a3622ba7c5a12c0bb486667698')}
    }


def test_list_all_leaf_node_paths(mock_hdfs_tree_paths: HdfsTreePaths):
    """Test function list_all_leaf_node_paths"""
    mock_hdfs_tree_paths.append_file_path("hdfs://hdfs_cluster/lake/")
    mock_hdfs_tree_paths.append_file_path("hdfs://hdfs_cluster/lake/encrypt/")
    mock_hdfs_tree_paths.append_file_path("hdfs://hdfs_cluster/lake/loyalty//20240302")
    mock_hdfs_tree_paths.append_file_path("hdfs://hdfs_cluster/lake/encrypt/  /202403/20240301")
    mock_hdfs_tree_paths.append_file_path("hdfs://hdfs_cluster/lake/encrypt/202403/20240302")
    mock_hdfs_tree_paths.append_file_path("hdfs://hdfs_cluster/lake/encrypt/ym=202403/ymd=20240302")
    mock_hdfs_tree_paths.append_file_path("hdfs://hdfs_cluster/lake/encrypt/ym=202403/ymd=20240302/event=e1")
    mock_hdfs_tree_paths.append_file_path("hdfs://hdfs_cluster/lake/ym=202403/ymd=20240302/event=e2")
    mock_hdfs_tree_paths.append_file_path("hdfs://hdfs_cluster/lake/ym=202403/ymd=20240302/event=e2/type=t2")
    mock_hdfs_tree_paths.append_file_path("ls: Permission denied: user=zdeploy")
    mock_hdfs_tree_paths.append_file_path("client_loop: send disconnect: Broken pipe")
    results = list(mock_hdfs_tree_paths.list_all_leaf_node_paths(
        current=mock_hdfs_tree_paths.root_node, path=mock_hdfs_tree_paths.domain
    ))
    assert len(results) == 5
    assert set(results) == {
        'hdfs://hdfs_cluster/lake/encrypt/202403/20240301',
        'hdfs://hdfs_cluster/lake/encrypt/202403/20240302',
        'hdfs://hdfs_cluster/lake/encrypt/ym=202403/ymd=20240302/event=e1',
        'hdfs://hdfs_cluster/lake/ym=202403/ymd=20240302/event=e2/type=t2',
        'hdfs://hdfs_cluster/lake/loyalty/20240302'
    }


if __name__ == "__main__":
    sys.exit(pytest.main([__file__] + sys.argv[1:]))
