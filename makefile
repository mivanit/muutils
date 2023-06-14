PACKAGE_NAME := muutils

VERSION_INFO_LOCATION := $(PACKAGE_NAME)/__init__.py
PUBLISH_BRANCH := main
PYPI_TOKEN_FILE := .pypi-token
LAST_VERSION_FILE := .lastversion
COVERAGE_REPORTS_DIR := docs/coverage
TESTS_DIR := tests/unit

VERSION := $(shell grep -oP '__version__ = "\K.*?(?=")' $(VERSION_INFO_LOCATION))
LAST_VERSION := $(shell cat $(LAST_VERSION_FILE))
PYPOETRY := poetry run python

.PHONY: default
default: help

.PHONY: version
version:
	@echo "Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)"
	@if [ "$(VERSION)" = "$(LAST_VERSION)" ]; then \
		echo "Python package $(VERSION) is the same as last published version $(LAST_VERSION), exiting!"; \
		exit 1; \
	fi

# at some point, need to add back --check-untyped-defs to mypy call
# but it complains when we specify arguments by keyword where positional is fine
# not sure how to fix this
# python -m pylint $(PACKAGE_NAME)/
# python -m pylint tests/
.PHONY: lint
lint: clean
	$(PYPOETRY) -m mypy --config-file pyproject.toml $(PACKAGE_NAME)/
	$(PYPOETRY) -m mypy --config-file pyproject.toml tests/

# formatting
# --------------------------------------------------
.PHONY: format
format:
	python -m pycln --config pyproject.toml --all .
	python -m isort format .
	python -m black .

.PHONY: check-format
check-format:
	@echo "run format check"
	python -m pycln --check --config pyproject.toml .
	python -m isort --check-only .
	python -m black --check .

# coverage reports
# --------------------------------------------------
.PHONY: cov
cov:
	@echo "generate text coverage report"
	$(PYPOETRY) -m coverage report -m > $(COVERAGE_REPORTS_DIR)/coverage.txt
	$(PYPOETRY) -m coverage_badge -f -o $(COVERAGE_REPORTS_DIR)/coverage.svg

.PHONY: cov-html
cov-html:
	@echo "generate html coverage report"
	$(PYPOETRY) -m coverage html	

# tests
# --------------------------------------------------

.PHONY: test
test: clean
	@echo "running tests"
	$(PYPOETRY) -m pytest --cov=. $(TESTS_DIR)

.PHONY: test-nocov
test-nocov: clean
	@echo "running tests, without code coverage"
	$(PYPOETRY) -m pytest tests

.PHONY: check
check: clean check-format clean test lint cov
	@echo "run format check, test, lint, and coverage report"

# build and publish
# --------------------------------------------------

.PHONY: verify-git
verify-git: 
	@echo "checking git status"
	if [ "$(shell git branch --show-current)" != $(PUBLISH_BRANCH) ]; then \
		echo "Git is not on the $(PUBLISH_BRANCH) branch, exiting!"; \
		exit 1; \
	fi; \
	if [ -n "$(shell git status --porcelain)" ]; then \
		echo "Git is not clean, exiting!"; \
		exit 1; \
	fi; \

.PHONY: build
build: 
	@echo "build via poetry, assumes checks have been run"
	poetry build

.PHONY: publish
publish: check build verify-git version
	@echo "run all checks, build, and then publish"

	@echo "Enter the new version number if you want to upload to pypi and create a new tag"
	@read -p "Confirm: " NEW_VERSION; \
	if [ "$$NEW_VERSION" != "$(VERSION)" ]; then \
		echo "Confirmation failed, exiting!"; \
		exit 1; \
	fi; \

	@echo "pypi username: __token__"
	@echo "pypi token from '$(PYPI_TOKEN_FILE)' :"
	echo $$(cat $(PYPI_TOKEN_FILE))

	echo "Uploading!"; \
	echo $(VERSION) > $(LAST_VERSION_FILE); \
	git add $(LAST_VERSION_FILE); \
	git commit -m "Auto update to $(VERSION)"; \
	git tag $(VERSION); \
	git push origin $(VERSION); \
	twine upload dist/* --verbose

# cleanup
# --------------------------------------------------

.PHONY: clean
clean:
	@echo "cleaning up"
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf $(PACKAGE_NAME).egg-info
	rm -rf tests/junk_data
	python -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

# listing targets, from stackoverflow
# https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: help
help:
	@echo -n "# list make targets"
	@echo ":"
	@cat Makefile | sed -n '/^\.PHONY: / h; /\(^\t@*echo\|^\t:\)/ {H; x; /PHONY/ s/.PHONY: \(.*\)\n.*"\(.*\)"/    make \1\t\2/p; d; x}'| sort -k2,2 |expand -t 25