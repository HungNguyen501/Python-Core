#!/usr/bin/env bash

RED="\033[0;31m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
NO_COLOR="\033[0m"

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
    tests=$(bazel query --keep_going --noshow_progress --output package "kind(test, ... - //configurations/lib/...)" 2>/dev/null)
    if [[ ! -z ${tests} ]];
    then
        make install
        printf "${GREEN}Running all tests...\n"; \
        printf '%.0s-' $(seq 1 50); \
        printf "\n${NO_COLOR}";
        for test in ${tests[@]}; do
            python3.11 -m pytest ${test} -vv --cov ${test} --cov-report term-missing --cov-fail-under=100
            if [ $? != 0 ]; then
                exit 1
            fi
        done
    else
        printf "${BLUE}No tests found\n"; \
        printf '%.0s-' $(seq 1 50); \
        printf "${NO_COLOR}\n";
    fi
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
        printf "${GREEN}Checking convention...\n"; \
        printf '%.0s-' $(seq 1 50); \
        printf "${NO_COLOR}\n";
        printf "${modules}\n"
        python3.11 -m flake8 ${modules} --show-source --statistics && python3.11 -m pylint ${modules}
        if [ $? != 0 ]; then
            exit 1
        fi
        tests=$(bazel query --keep_going --noshow_progress --output package  "kind(test, rdeps(//..., set(${files[*]})))" 2>/dev/null)
        if [[ ! -z ${tests} ]]; then
            printf "${GREEN}Running tests...\n"; \
            printf '%.0s-' $(seq 1 50); \
            printf "${NO_COLOR}\n";
            for test in ${tests[@]}; do
                python3.11 -m pytest ${test} -vv --cov ${test} --cov-report term-missing --cov-fail-under=100
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
    echo "Check convention..."
    python3.11 -m flake8 ${1} --show-source --statistics && python3.11 -m pylint ${1}
}
run_unit_tests () {
    echo "Run unit tests..."
    python3.11 -m pytest ${1} -vv --cov ${1} --cov-report term-missing --cov-fail-under=100
}
# Execute function
$*
