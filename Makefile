ProjectName := Python-Core

install:
	@python3 --version
	@python3 -m pip install --upgrade pip
	@python3 -m pip install -r ./requirements.txt

test:
	@bash ./validators.sh run_unit_tests

pep8:
	@bash ./validators.sh check_pep8

check_ref_name:
	@bash ./validators.sh validate_ref_name $(REF_TYPE) $(REF_NAME)

skip_checking:
	@bash ./validators.sh skip_convention_checking $(CHANGES)
