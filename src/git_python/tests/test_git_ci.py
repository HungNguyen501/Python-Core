"""Test git_ci module"""
import sys
from unittest.mock import patch, call, MagicMock

from click.testing import CliRunner
import pytest
from src.git_python.git_ci import (
    get_changed_files_of_commit,
    skip_convention_checking,
    main
)


def test_get_changed_files_of_commit():
    """Test get_changed_files_of_commit function"""
    mock_repo = MagicMock()
    mock_commit = MagicMock()
    mock_commit.stats.files = {"dum1": 1, "dum2": 0}
    mock_repo.iter_commits = MagicMock(return_value=[mock_commit])
    files = get_changed_files_of_commit(repo=mock_repo, back_head_to=0,)
    assert files == ["dum1", "dum2"]


@patch(target="src.git_python.git_ci.sys.exit")
def test_skip_convention_checking(mock_exit):
    """Test skip_convention_checking function"""
    mock_repo = MagicMock()
    mock_repo.commit.return_value.stats. \
        files.keys.side_effect = [
            ["foo/dum1.md", "foo/dum2.ipynb"],
            ["foo/dum1.md", "foo/dum2.py"],
        ]
    # Case: return exit 1 to skip convention checking
    skip_convention_checking(repo=mock_repo, commit_hash="xyz",)
    assert mock_exit.mock_calls == [call(1)]
    # Case: return exit 0 to continue pipelinse
    skip_convention_checking(repo=mock_repo, commit_hash="xyz",)
    assert mock_exit.mock_calls == [call(1), call(0), call(1)]


@patch(target="src.git_python.git_ci.skip_convention_checking")
@patch(target="src.git_python.git_ci.Repo")
def test_main(mock_repo, *_):
    """Test main function"""
    runner = CliRunner()
    runner.invoke(main, ["-f", "skip_convention_checking", "-c", "xyz",])
    assert mock_repo.mock_calls == [call(path='./')]


if __name__ == "__main__":
    sys.exit(pytest.main([__file__] + sys.argv[1:]))
