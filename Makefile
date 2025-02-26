ProjectName := Python-Core
CiScript := ci/ci.sh
GithookScript := ci/githooks.sh
PythonVersion := python3.12

init:
	@bash ./$(GithookScript) create_pre_commit_file
	@$(PythonVersion) --version
	@$(PythonVersion) -m pip install --upgrade pip --break-system-packages
	@$(PythonVersion) -m pip install -r ./ci/requirements.txt --break-system-packages
	@$(PythonVersion) -m pip install -r ./build/requirements.txt --break-system-packages

test:
	@bash ./$(CiScript) run_unit_tests $(LOCATION)

pep8:
	@bash ./$(CiScript) check_pep8 $(LOCATION)

verify_changes:
	@bash ./$(CiScript) verify_changes $(CHANGES)
	@bazel clean --async

test_integration:
	@bash ./$(CiScript) test_integration $(SERVICE)

test_all:
	@bash ./$(CiScript) run_all_tests

.DEFAULT_GOAL := help
.PHONY: help
all: help
help: Makefile
	@echo $(ProjectName)
