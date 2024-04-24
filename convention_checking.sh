#!/usr/bin/env bash
check_pep8 () {
    echo "Check convention..."
    python3 -m flake8 . --show-source --statistics && python3 -m pylint src
}
run_unit_tests () {
    echo "Run unit tests..."
    python3 -m pytest -vv --cov ./src --cov-report term-missing --cov-fail-under=100
}
if [ -z "${1}" ]; then
    check_pep8
    run_unit_tests
elif [ ${1} == "PEP8" ]; then
    check_pep8
elif [ ${1} == "TEST" ]; then
    run_unit_tests
else
    echo "Type wrong job name (PEP8 or TEST), please retry."
    exit 1
fi
