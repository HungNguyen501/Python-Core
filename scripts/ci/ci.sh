#!/usr/bin/env bash

PYTHON='python3'

[[ -z "${ENVIRONMENT}" ]] && ENVIRONMENT="local" || ENVIRONMENT=${ENVIRONMENT}

function install_deps () {
    ALLOWED_ENVS=("dev" "prod")
    if [[ " ${ALLOWED_ENVS[*]} " =~ " ${ENVIRONMENT} " ]]; then
        ${PYTHON} --version
        echo ">> Installing dependencies..."
        ${PYTHON} -m pip install --upgrade pip --break-system-packages --quiet
        cat ./scripts/ci/requirements-ci.txt
        ${PYTHON} -m pip install -r ./scripts/ci/requirements.txt --break-system-packages --quiet
    fi
}

function pep8 () {
    if [[ -z ${1} ]]; then
        echo "Empty path!"
        return 0
    fi
    echo ">> Checking PEP8 at ${1}"
    ${PYTHON} -m flake8 ${1} --show-source --statistics && ${PYTHON} -m pylint ${1}
    if [ $? != 0 ]; then
        exit 1
    fi
}

function run_tests () {
    if [[ -z ${1} ]]; then
        echo "Empty path!"
        return 0
    else
        location=${1}
    fi
    install_deps
    echo ">> Running tests at ${location}"
    ${PYTHON} -m pytest ${location} \
        --disable-warnings \
        -vv \
        --cov ${location} \
        --cov-report term-missing \
        --cov-fail-under=100 \
        -m "not integration_tests"  # Exclude marked tests
    if [ $? != 0 ]; then
        exit 1
    fi
}

function verify_changes () {
    if [[ -z ${1} ]]; then
        echo "Empty changes!"
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
        tests=$(bazel query \
            --keep_going \
            --noshow_progress \
            "kind(test, rdeps(//..., set(${files[*]})))" 2>/dev/null)
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

function test_integration () {
    docker compose -f docker-compose.yml up -d pool_api
    ${PYTHON} -m pytest src/ \
        --disable-warnings \
        -vv \
        -m integration_tests
}

# Execute function
$*
