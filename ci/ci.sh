#!/usr/bin/env bash

RED="\033[0;31m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
NO_COLOR="\033[0m"

PYTHON='python3.11'

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
run_all_tests () {
    make install
    check_pep8 src/
    run_unit_tests src/
}
run_ci () {
    if [[ -z ${1} ]]; then
        printf "${BLUE}Input(CHANGES) is empty.${NO_COLOR}\n";
        return 0
    fi
    files=()
    IFS=',' read -r -a changed_files <<< "${1}"
    for file_name in ${changed_files[@]}; do
        files+=("$(bazel query --keep_going --noshow_progress "${file_name}" 2>/dev/null) ")
    done
    modules=$(bazel query --noshow_progress --output package "set(${files[*]})" 2>/dev/null)
    if [[ ! -z ${modules} ]]; then
        make install
        printf "${GREEN}Checking PEP8 convention...\n";
        printf '%.0s-' $(seq 1 50);
        printf "${NO_COLOR}\n";
        printf "${modules}\n"
        ${PYTHON} -m flake8 ${modules} --show-source --statistics && ${PYTHON} -m pylint ${modules}
        if [ $? != 0 ]; then
            exit 1
        fi
        tests=$(bazel query --keep_going --noshow_progress --output package  "kind(test, rdeps(//..., set(${files[*]})))" 2>/dev/null)
        if [[ ! -z ${tests} ]]; then
            printf "${GREEN}Running tests...\n"; \
            printf '%.0s-' $(seq 1 50); \
            printf "${NO_COLOR}\n";
            for test in ${tests[@]}; do
                ${PYTHON} -m pytest ${test} \
                    --disable-warnings \
                    -vv \
                    --cov ${test} \
                    --cov-report term-missing \
                    --cov-fail-under=100
                if [ $? != 0 ]; then
                    exit 1
                fi
            done
        else
            printf "${BLUE}No tests found\n"; \
            printf '%.0s-' $(seq 1 50); \
            printf "${NO_COLOR}\n";
        fi
    else
        printf "${BLUE}Changes take no effect\n"; \
        printf '%.0s-' $(seq 1 50); \
        printf "${NO_COLOR}\n";
    fi
}
check_pep8 () {
    printf "${GREEN}Checking PEP8 convention in ${1}...\n"
    printf '%.0s-' $(seq 1 50)
    printf "${NO_COLOR}\n"
    ${PYTHON} -m flake8 ${1} --show-source --statistics && ${PYTHON} -m pylint ${1}
    if [ $? != 0 ]; then
        exit 1
    fi
}
run_unit_tests () {
    printf "${GREEN}Running unit tests in ${1}...\n"
    printf '%.0s-' $(seq 1 50)
    printf "${NO_COLOR}\n"
    ${PYTHON} -m pytest ${1} -vv --cov ${1} --cov-report term-missing --cov-fail-under=100
    if [ $? != 0 ]; then
        exit 1
    fi
}
# Execute function
$*
