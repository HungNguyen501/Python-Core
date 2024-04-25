#!/usr/bin/env bash
validate_ref_name () {
    ref_type=${1}
    ref_name=${2}
    if [ "${ref_type}" == "tag" ] ||
        { 
            [ "${ref_type}" == "branch" ] && 
            [[ "${ref_name}" == "main"  || ${ref_name} == feature/* ]]
        };
    then
        echo "Branch name is qualified: ${ref_name}"
        exit 0
    else
        echo "Branch name is invalid: ${ref_name}. It should be started with [feature/]"
        exit 1
    fi
}
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
elif [ ${1} == "REF" ]; then
    validate_ref_name ${2} ${3}
else
    echo "Type wrong job name (PEP8, TEST or REF), please retry."
    exit 1
fi
