ProjectName := Python-Core
CiScript := scripts/ci/ci.sh
GithookScript := scripts/ci/githooks.sh
PythonVersion := python3

init:
	@bash ./$(GithookScript) create_pre_commit_file
	@$(PythonVersion) --version
	@$(PythonVersion) -m pip install --upgrade pip --break-system-packages
	@$(PythonVersion) -m pip install -r ./scripts/ci/requirements-ci.txt --break-system-packages
	@$(PythonVersion) -m pip install -r ./scripts/build/requirements.txt --break-system-packages

test:
	@bash ./$(CiScript) run_tests $(path)

pep8:
	@bash ./$(CiScript) pep8 $(path)

verify_changes:
	@bash ./$(CiScript) verify_changes $(paths)
	@bazel clean --async

test_integration:
	@bash ./$(CiScript) test_integration

.DEFAULT_GOAL := help
.PHONY: help
all: help
help: Makefile
	@echo $(ProjectName)
