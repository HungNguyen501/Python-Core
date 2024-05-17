ProjectName := Python-Core

install:
	@python3 --version
	@python3 -m pip install --upgrade pip
	@python3 -m pip install -r ./requirements.txt

test:
	@bash ./validators.sh run_unit_tests $(LOCATION)

pep8:
	@bash ./validators.sh check_pep8 $(LOCATION)

check_ref_name:
	@bash ./validators.sh validate_ref_name $(REF_TYPE) $(REF_NAME)

run_ci:
	@bash ./validators.sh run_ci $(CHANGES)
	@bazel clean --async
