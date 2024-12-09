#!/usr/bin/env bash

PYTHON='python3.12'
[[ -z "${ENVIRONMENT}" ]] && ENVIRONMENT="local" || ENVIRONMENT=${ENVIRONMENT}

install () {
    ALLOWED_ENVS=("dev" "prod")
    if [[ " ${ALLOWED_ENVS[*]} " =~ " ${ENVIRONMENT} " ]]; then
        ${PYTHON} --version
        echo "Installing..."
        ${PYTHON} -m pip install --upgrade pip --break-system-packages --quiet
        ${PYTHON} -m pip install -r ./ci/requirements.txt --break-system-packages --quiet
    fi
}
check_pep8 () {
    if [[ -z ${1} ]]; then
        printf "Please input LOCATION for checking.\n";
        return 0
    fi
    printf "[Checking PEP8 convention in ${1}...]\n"
    ${PYTHON} -m flake8 ${1} --show-source --statistics && ${PYTHON} -m pylint ${1}
    if [ $? != 0 ]; then
        exit 1
    fi
}
run_unit_tests () {
    if [[ -z ${1} ]]; then
        printf "Please input LOCATION for testing.\n";
        return 0
    fi
    printf "[Running tests in ${1}...]\n"
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
verify_changes () {
    if [[ -z ${1} ]]; then
        printf "Input(CHANGES) is empty.\n";
        return 0
    fi
    files=()
    IFS=',' read -r -a changed_files <<< "${1}"
    for file_name in ${changed_files[@]}; do
        files+=("$(bazel query --keep_going --noshow_progress "${file_name}" 2>/dev/null) ")
    done
    modules=$(bazel query --noshow_progress --output package "set(${files[*]})" 2>/dev/null)
    if [[ ! -z ${modules} ]]; then
        install
        check_pep8 ${modules}
        tests=$(bazel query --keep_going --noshow_progress --output package  "kind(test, rdeps(//..., set(${files[*]})))" 2>/dev/null)
        if [[ ! -z ${tests} ]]; then
            for test in ${tests[@]}; do
                run_unit_tests ${test}
            done
        else
            printf "No test found.\n"
        fi
    else
        printf "Changes take no effect.\n"
    fi
}
run_all_tests () {
    install
    check_pep8 src/
    run_unit_tests src/
}
test_integration () {
    if [[ -z ${1} ]]; then
        printf "Input(SERVICE) is empty.\n";
        return 0
    fi
    set -e
    export INTEGRATION_TEST="ENABLE"
    case "${1}" in
        "pool_api")
            docker compose -f build/docker-compose.yml up -d pool_api
            run_unit_tests src/pool_api/integration_tests
            docker container stop pool_api
            ;;
        *)
            echo "Service not found!"
            ;;
    esac
}
# Execute function
$*
