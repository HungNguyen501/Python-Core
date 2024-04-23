#!/usr/bin/env bash
check_pep8 () {
    echo "Check convention..."
    python3 -m flake8 . --count --show-source --statistics && python3 -m pylint unittest_async hdfs_tree_paths data_hub
}
run_unit_tests () {
    echo "Run unit tests..."
    python3 -m pytest -vv --cov ./ --cov-report term-missing --cov-fail-under=100
}
if [ -z "${1}" ]; then
    check_pep8
    run_unit_tests
fi
JOB_NAME=${1}
if [ ${JOB_NAME} == "PEP8" ]; then
    check_pep8
elif [ ${JOB_NAME} == "TEST" ]; then
    run_unit_tests
else
    echo "Type wrong job name (PEP8 or TEST), please retry."
    exit 1
fi
