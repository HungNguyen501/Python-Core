"""Test git_ci module"""
from unittest.mock import patch, call, MagicMock

from click.testing import CliRunner
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
    mock_repo.git.diff.side_effect = [
        "fool1/dum.md\nfool2/dum.ipynb",
        "fool1/dum.md\nfool2/dum.py",
    ]
    mock_commit = MagicMock()
    mock_commit.__next__.side_effect = ["abc", "xyz", "abc", "xyz",]
    mock_repo.iter_commits = MagicMock(return_value=mock_commit)
    # Case: return exit 1 to skip convention checking
    skip_convention_checking(repo=mock_repo,)
    assert mock_exit.mock_calls == [call(1)]
    # Case: return exit 0 to continue pipelinse
    skip_convention_checking(repo=mock_repo,)
    assert mock_exit.mock_calls == [call(1), call(0), call(1)]


@patch(target="src.git_python.git_ci.skip_convention_checking")
@patch(target="src.git_python.git_ci.Repo")
def test_main(mock_repo, *_):
    """Test main function"""
    runner = CliRunner()
    runner.invoke(main, ["-f", "skip_convention_checking",])
    assert mock_repo.mock_calls == [call(path='./')]
