THIS_DIR := $(dir $(MAKEFILE_LIST))
COVERAGE_RC := $(THIS_DIR)backend/tests/.coveragerc
MANAGE_PY := $(THIS_DIR)backend/core/manage.py

code-check:
	pylint --rcfile $(THIS_DIR)pep8/.pylintrc backend

run:
	python $(MANAGE_PY) my_runserver

migrate:
	python $(MANAGE_PY) makemigrations
	python $(MANAGE_PY) migrate


test:
	coverage run --rcfile=$(COVERAGE_RC) $(MANAGE_PY) test backend
	coverage report

generate-test-html-report:
	coverage html --rcfile=$(COVERAGE_RC)
