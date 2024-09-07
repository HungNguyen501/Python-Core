ProjectName := Python-Core
CiScript := ci/ci.sh
GithookScript := ci/githooks.sh

githook:
	@bash ./$(GithookScript) create_pre_commit_file

install:
	@python3.11 --version
	@python3.11 -m pip install --upgrade pip
	@python3.11 -m pip install -r ./ci/requirements.txt

test:
	@bash ./$(CiScript) run_unit_tests $(LOCATION)

pep8:
	@bash ./$(CiScript) check_pep8 $(LOCATION)

check_ref_name:
	@bash ./$(CiScript) validate_ref_name $(REF_TYPE) $(REF_NAME)

test_all:
	@bash ./$(CiScript) run_all_tests

run_ci:
	@bash ./$(CiScript) run_ci $(CHANGES)
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
