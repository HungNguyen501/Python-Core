#!/usr/bin/env bash
echo "Check convention ..."
python3 -m flake8 && python3 -m pylint unittest_async hdfs_tree_paths data_hub
echo "Unit tests ..."
python3 -m pytest -vv --cov ./ --cov-report term-missing --cov-fail-under=100
