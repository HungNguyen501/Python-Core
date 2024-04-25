"""CI scritps for GitHub"""
import sys
from typing import List, Dict

import click
from git import Repo


def get_changed_files_of_commit(repo: Repo, back_head_to: int) -> List[Dict]:
    """List changed files of a specific commit that behinds HEAD

    Args:
        repo(Repo): Git Repo Object
        back_to_head(int): the number points to diffrent of positions between HEAD and commit

    Return list changed files
    """
    list_commits = list(repo.iter_commits())
    return list(list_commits[back_head_to].stats.files.keys())


def skip_convention_checking(repo: Repo,):
    """Verify changed files of last commit to determine skip
    to check convention or not.
    If all changed files is in list of ignore pattern then exit program with success code
    else then exit program with error code

    Args:
        repo(Repo): GitHub repo Object
        commit_hash(str): commit SHA value or HEAD~1..HEAD
    """
    commits = repo.iter_commits()
    last_commit = str(next(commits))
    old_commit = str(next(commits))
    changed_files = repo.git.diff(old_commit, last_commit, name_only=True).splitlines()
    list_ignored_files = [".md", ".ipynb",]
    for file in changed_files:
        if not any(ig in file for ig in list_ignored_files):
            sys.exit(0)
    print("Skip pipelines for convention checking beacause it includes:")
    print(*changed_files, sep="\n",)
    sys.exit(1)


@click.command()
@click.option(
    '-f', '--function',
    type=str,
    default=None,
    help='Choose a function in git-ci'
)
def main(function):
    """Run main program"""
    repo = Repo(path="./")
    list_functions = {
        "skip_convention_checking": skip_convention_checking,
    }
    list_functions[function](repo=repo,)


if __name__ == "__main__":
    main()
