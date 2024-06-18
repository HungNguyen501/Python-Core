#!/usr/bin/env bash

RED="\033[0;31m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
NO_COLOR="\033[0m"

PYTHON='python3.11'

validate_ref_name () {
    ref_type=${1}
    ref_name=${2}
    branch_pattern="^main$|^feature/.+$"
    tag_pattern="^test-all-v[0-9]+$"
    if [ "${ref_type}" == "branch" ]; then
        if [[ "${ref_name}" =~ ${branch_pattern} ]]; then
            printf "${GREEN}Branch name is qualified: ${ref_name}.${NO_COLOR}\n";
            exit 0
        fi
        printf "${RED}Branch name is invalid: ${ref_name}. It should be main or started with [feature/*].${NO_COLOR}\n"
        exit 1
    elif [ "${ref_type}" == "tag" ]; then
        if [[ "${ref_name}" =~ ${tag_pattern} ]]; then
            printf "${GREEN}Tag name is qualified: ${ref_name}.${NO_COLOR}\n"
            exit 0
        fi
        printf "${RED}Tag name is invalid: ${ref_name}. It should be started with [test-all-v*].${NO_COLOR}\n"
        exit 1
    else
        printf "${RED}ref_type is invalid: ${ref_type}. Valid values are [branch, tag].${NO_COLOR}\n"
        exit 1 
    fi
}
check_pep8 () {
    if [[ -z ${1} ]]; then
        printf "${BLUE}Please input LOCATION for checking.${NO_COLOR}\n";
        return 0
    fi
    printf "${GREEN}Checking PEP8 convention in ${1}...\n"
    printf '%.0s-' $(seq 1 50)
    printf "${NO_COLOR}\n"
    ${PYTHON} -m flake8 ${1} --show-source --statistics && ${PYTHON} -m pylint ${1}
    if [ $? != 0 ]; then
        exit 1
    fi
}
run_unit_tests () {
    if [[ -z ${1} ]]; then
        printf "${BLUE}Please input LOCATION for testing.${NO_COLOR}\n";
        return 0
    fi
    printf "${GREEN}Running unit tests in ${1}...\n"
    printf '%.0s-' $(seq 1 50)
    printf "${NO_COLOR}\n"
    ${PYTHON} -m pytest ${1} \
        --disable-warnings \
        -vv \
        --cov ${1} \
        --cov-report term-missing \
        --cov-fail-under=100
    if [ $? != 0 ]; then
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
        check_pep8 ${modules}
        tests=$(bazel query --keep_going --noshow_progress --output package  "kind(test, rdeps(//..., set(${files[*]})))" 2>/dev/null)
        if [[ ! -z ${tests} ]]; then
            for test in ${tests[@]}; do
                run_unit_tests ${test}
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
# Execute function
$*
