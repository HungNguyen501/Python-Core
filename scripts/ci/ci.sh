#!/usr/bin/env bash

PYTHON='python3.12'

[[ -z "${ENVIRONMENT}" ]] && ENVIRONMENT="local" || ENVIRONMENT=${ENVIRONMENT}

install_deps () {
    ALLOWED_ENVS=("dev" "prod")
    if [[ " ${ALLOWED_ENVS[*]} " =~ " ${ENVIRONMENT} " ]]; then
        ${PYTHON} --version
        echo ">> Installing..."
        ${PYTHON} -m pip install --upgrade pip --break-system-packages --quiet
        ${PYTHON} -m pip install -r ./scripts/ci/requirements.txt --break-system-packages --quiet
    fi
}

pep8 () {
    if [[ -z ${1} ]]; then
        printf "Input(LOCATION) is empty.\n";
        return 0
    fi
    echo ">> Checking PEP8 at ${1}"
    ${PYTHON} -m flake8 ${1} --show-source --statistics && ${PYTHON} -m pylint ${1}
    if [ $? != 0 ]; then
        exit 1
    fi
}

run_tests () {
    if [[ -z ${1} ]]; then
        printf "Input(LOCATION) is empty.\n";
        return 0
    fi
    echo ">> Running tests at ${1}"
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
    IFS=',' read -r -a input_files <<< "${1}"
    for file in ${input_files[@]}; do
        files+=("$(bazel query --keep_going --noshow_progress "${file}" 2>/dev/null) ")
    done
    packages=$(bazel query --noshow_progress --output package "set(${files[*]})" 2>/dev/null)
    if [[ ! -z ${packages} ]]; then
        install_deps
        pep8 ${packages}
        tests=$(bazel query --keep_going --noshow_progress --output package  "kind(test, rdeps(//..., set(${files[*]})))" 2>/dev/null)
        if [[ ! -z ${tests} ]]; then
            for test in ${tests[@]}; do
                run_tests ${test}
            done
        else
            echo "No test found!"
        fi
    else
        echo "Changes take no effect!"
        # Create empty path to avoid Error: Cache folder path is retrieved for pip but doesn't exist on disk: /home/runner/.cache/pip
        mkdir -p ~/.cache/pip
    fi
}

test_integration () {
    if [[ -z ${1} ]]; then
        echo "Input(SERVICE) is empty";
        return 0
    fi
    set -e
    export INTEGRATION_TEST="ENABLE"
    case "${1}" in
        "pool_api")
            docker compose -f scripts/build/docker-compose.yml up -d pool_api
            run_tests src/pool_api/integration_tests
            docker container stop pool_api
            ;;
        *)
            echo "Service not found!"
            ;;
    esac
}

# Execute function
$*
