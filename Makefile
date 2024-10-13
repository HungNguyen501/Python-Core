ProjectName := Python-Core
CiScript := ci/ci.sh
GithookScript := ci/githooks.sh
PythonVersion := python3

githook:
	@bash ./$(GithookScript) create_pre_commit_file

install:
	@$(PythonVersion) --version
	@$(PythonVersion) -m pip install --upgrade pip --break-system-packages
	@$(PythonVersion) -m pip install -r ./ci/requirements.txt --break-system-packages

test:
	@bash ./$(CiScript) run_unit_tests $(LOCATION)

pep8:
	@bash ./$(CiScript) check_pep8 $(LOCATION)

check_ref_name:
	@bash ./$(CiScript) validate_ref_name $(REF_TYPE) $(REF_NAME)

test_all:
	@bash ./$(CiScript) run_all_tests

verify_changes:
	@bash ./$(CiScript) verify_changes $(CHANGES)
	@bazel clean --async

build_pool_api:
	@docker compose -f build/docker-compose.yml up -d pool_api

build_postgres_db:
	@docker compose -f build/docker-compose.yml up -d postgres_db

.DEFAULT_GOAL := help
.PHONY: help
all: help
help: Makefile
	@echo "Hello World!"
