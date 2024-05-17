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
run_ci () {
    files=()
    IFS=',' read -r -a changed_files <<< "${1}"
    for file_name in ${changed_files[@]}; do
        files+=("$(bazel query --keep_going --noshow_progress "$file_name") ")
    done
    modules=$(bazel query --noshow_progress --output package "set(${files[*]})" )
    if [[ ! -z ${modules} ]]; then
        make install
        printf "Check convention...\n${modules}\n"
        python3 -m flake8 ${modules} --show-source --statistics && python3 -m pylint ${modules}
        if [ $? != 0 ]; then
            exit 1
        fi
        tests=$(bazel query --keep_going --noshow_progress --output package  "kind(test, rdeps(//..., set(${files[*]})))")
        printf "Run unit tests...\n${tests}\n"
        if [[ ! -z $tests ]]; then
            for test in ${tests[@]}; do
                python3 -m pytest ${test} -vv --cov ${test} --cov-report term-missing --cov-fail-under=100
                if [ $? != 0 ]; then
                    exit 1
                fi
            done
        fi
    else
        echo "----------Skip convention checking----------"
        exit 0
    fi
}
check_pep8 () {
    echo "Check convention..."
    python3 -m flake8 ${1} --show-source --statistics && python3 -m pylint ${1}
}
run_unit_tests () {
    echo "Run unit tests..."
    python3 -m pytest ${1} -vv --cov ${1} --cov-report term-missing --cov-fail-under=100
}
# Execute function
$*
