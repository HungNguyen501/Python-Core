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
trigger_ci () {
    files=()
    IFS=',' read -r -a changed_files <<< "${1}"
    for file_name in ${changed_files[@]}; do
        files+=("$(bazel query --keep_going --noshow_progress "$file")")
    done
    if [ ${#files[@]} < 0 ];
    then
        echo "Skip convention checking."
        exit 0
    fi
    # Check convention
    modules=$(bazel query --keep_going --noshow_progress --output package "set(${files[*]})" )
    if [[ ! -z $tests ]]; then
        make install
        echo "Check convention..."
        python3 -m flake8 ${modules} --show-source --statistics && python3 -m pylint ${modules}
    fi
    # Run unit tests
    tests=$(bazel query --keep_going --noshow_progress "kind(test, rdeps(//..., set(${files[*]})))")
    if [[ ! -z $tests ]]; then
        bazel test --verbose_failures  --test_verbose_timeout_warnings --test_output=all $tests
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
