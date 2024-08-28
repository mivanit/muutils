# configuration
# ==================================================
# it assumes that the source is in a directory named the same as the package name
PACKAGE_NAME := muutils

# for checking you are on the right branch when publishing
PUBLISH_BRANCH := main
# where to put docs
DOCS_DIR := docs
# where to put the coverage reports
COVERAGE_REPORTS_DIR := docs/coverage
# where the tests are (assumes pytest)
TESTS_DIR := tests/unit
# temp directory to clean up
TESTS_TEMP_DIR := tests/_temp
# dev and lint requirements.txt files
REQ_DEV := .github/dev-requirements.txt
REQ_LINT := .github/lint-requirements.txt

# probably don't change these:
# --------------------------------------------------
# will print this token when publishing
PYPI_TOKEN_FILE := .github/local/.pypi-token
# the last version that was auto-uploaded. will use this to create a commit log for version tag
LAST_VERSION_FILE := .github/.lastversion
# where the pyproject.toml file is
PYPROJECT := pyproject.toml
# base python to use. Will add `poetry run` in front of this if `RUN_GLOBAL` is not set to 1
PYTHON_BASE := python
# where the commit log will be stored
COMMIT_LOG_FILE := .github/local/.commit_log
# pandoc commands (for docs)
PANDOC ?= pandoc


# reading information and command line options
# ==================================================

# RUN_GLOBAL=1 to use global `PYTHON_BASE` instead of `poetry run $(PYTHON_BASE)`
# --------------------------------------------------
# for formatting, we might want to run python without setting up all of poetry
RUN_GLOBAL ?= 0
ifeq ($(RUN_GLOBAL),0)
	PYTHON = poetry run $(PYTHON_BASE)
else
	PYTHON = $(PYTHON_BASE)
endif

# reading version
# --------------------------------------------------
# assuming your pyproject.toml has a line that looks like `version = "0.0.1"`, will get the version
VERSION := NULL
# read last auto-uploaded version from file
LAST_VERSION := NULL
# get the python version, now that we have picked the python command
PYTHON_VERSION := NULL
.PHONY: gen-version-info
gen-version-info:
	$(eval VERSION := $(shell python -c "import re; print('v'+re.search(r'^version\s*=\s*\"(.+?)\"', open('$(PYPROJECT)').read(), re.MULTILINE).group(1))") )
	$(eval LAST_VERSION := $(shell [ -f $(LAST_VERSION_FILE) ] && cat $(LAST_VERSION_FILE) || echo NULL) )
	$(eval PYTHON_VERSION := $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')") )

# getting commit log
.PHONY: gen-commit-log
gen-commit-log: gen-version-info
	if [ "$(LAST_VERSION)" = "NULL" ]; then \
		echo "LAST_VERSION is NULL, cant get commit log!"; \
		exit 1; \
	fi
	$(shell python -c "import subprocess; open('$(COMMIT_LOG_FILE)', 'w').write('\n'.join(reversed(subprocess.check_output(['git', 'log', '$(LAST_VERSION)'.strip() + '..HEAD', '--pretty=format:- %s (%h)']).decode('utf-8').strip().split('\n'))))")

	
# loose typing, allow warnings for python <3.10
# --------------------------------------------------
TYPECHECK_ARGS ?= 
# COMPATIBILITY_MODE: whether to run in compatibility mode for python <3.10
COMPATIBILITY_MODE := $(shell $(PYTHON) -c "import sys; print(1 if sys.version_info < (3, 10) else 0)")

# options we might want to pass to pytest
# --------------------------------------------------
PYTEST_OPTIONS ?= # using ?= means you can pass extra options from the command line
COV ?= 1

ifdef VERBOSE
	PYTEST_OPTIONS += --verbose
endif

ifeq ($(COV),1)
    PYTEST_OPTIONS += --cov=.
endif

# compatibility mode for python <3.10
# --------------------------------------------------

# whether to run pytest with warnings as errors
WARN_STRICT ?= 0

ifneq ($(WARN_STRICT), 0)
    PYTEST_OPTIONS += -W error
endif

# Update the PYTEST_OPTIONS to include the conditional ignore option
ifeq ($(COMPATIBILITY_MODE), 1)
	JUNK := $(info !!! WARNING !!!: Detected python version less than 3.10, some behavior will be different)
    PYTEST_OPTIONS += --ignore=tests/unit/validate_type/
	TYPECHECK_ARGS += --disable-error-code misc --disable-error-code syntax --disable-error-code import-not-found
endif


# default target (help)
# ==================================================

.PHONY: default
default: help

.PHONY: version
version: gen-commit-log
	@echo "Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)"
	@echo "Commit log since last version:"
	@cat $(COMMIT_LOG_FILE)
	@if [ "$(VERSION)" = "$(LAST_VERSION)" ]; then \
		echo "Python package $(VERSION) is the same as last published version $(LAST_VERSION), exiting!"; \
		exit 1; \
	fi


# formatting
# ==================================================

.PHONY: setup-format
setup-format:
	@echo "install only packages needed for formatting, direct via pip (useful for CI)"
	$(PYTHON) -m pip install -r $(REQ_LINT)

.PHONY: format
format:
	@echo "format the source code"
	$(PYTHON) -m ruff format --config $(PYPROJECT) .
	$(PYTHON) -m ruff check --fix --config $(PYPROJECT) .
	$(PYTHON) -m pycln --config $(PYPROJECT) --all .

.PHONY: check-format
check-format:
	@echo "run format check"
	$(PYTHON) -m ruff check --config $(PYPROJECT) .
	$(PYTHON) -m pycln --check --config $(PYPROJECT) .

# coverage & docs
# ==================================================

.PHONY: docs-html
docs-html:
	@echo "generate html docs"
	$(PYTHON) docs/make_docs.py

.PHONY: docs-md
docs-md:
	@echo "generate combined docs in markdown"
	$(PYTHON) docs/make_docs.py --combined


.PHONY: docs-combined
docs-combined: docs-md
	@echo "generate combined docs in markdown and other formats"
	@echo "requires pandoc in path"
	$(PANDOC) -f markdown -t gfm $(DOCS_DIR)/combined/$(PACKAGE_NAME).md -o $(DOCS_DIR)/combined/$(PACKAGE_NAME)_gfm.md
	$(PANDOC) -f markdown -t plain $(DOCS_DIR)/combined/$(PACKAGE_NAME).md -o $(DOCS_DIR)/combined/$(PACKAGE_NAME).txt
	$(PANDOC) -f markdown -t html $(DOCS_DIR)/combined/$(PACKAGE_NAME).md -o $(DOCS_DIR)/combined/$(PACKAGE_NAME).html --embed-resources

# $(PANDOC) -f markdown -t pdf $(DOCS_DIR)/combined/$(PACKAGE_NAME).md -o $(DOCS_DIR)/combined/$(PACKAGE_NAME).pdf


.PHONY: cov
cov:
	@echo "generate coverage reports"
	$(PYTHON) -m coverage report -m > $(COVERAGE_REPORTS_DIR)/coverage.txt
	$(PYTHON) -m coverage_badge -f -o $(COVERAGE_REPORTS_DIR)/coverage.svg
	$(PYTHON) -m coverage html --directory=$(COVERAGE_REPORTS_DIR)/html/
	rm -rf $(COVERAGE_REPORTS_DIR)/html/.gitignore

.PHONY: docs
docs: cov docs-html docs-combined
	@echo "generate all documentation"

.PHONY: clean-docs
clean-docs:
	@echo "clean up docs"
	rm -rf $(DOCS_DIR)/combined/
	rm -rf $(DOCS_DIR)/muutils/
	rm -rf $(COVERAGE_REPORTS_DIR)
	rm $(DOCS_DIR)/muutils.html
	rm $(DOCS_DIR)/index.html
	rm $(DOCS_DIR)/search.js



# tests
# ==================================================

.PHONY: gen-extra-tests
gen-extra-tests:
	if [ $(COMPATIBILITY_MODE) -eq 0 ]; then \
		echo "converting certain tests to modern format"; \
		$(PYTHON) tests/util/replace_type_hints.py tests/unit/validate_type/test_validate_type.py "# DO NOT EDIT, GENERATED FILE" > tests/unit/validate_type/test_validate_type_GENERATED.py; \
	fi; \

# at some point, need to add back --check-untyped-defs to mypy call
# but it complains when we specify arguments by keyword where positional is fine
# not sure how to fix this
# python -m pylint $(PACKAGE_NAME)/
# python -m pylint tests/
.PHONY: typing
typing: clean gen-extra-tests
	@echo "running type checks"
	$(PYTHON) -m mypy --config-file $(PYPROJECT) $(TYPECHECK_ARGS) $(PACKAGE_NAME)/
	$(PYTHON) -m mypy --config-file $(PYPROJECT) $(TYPECHECK_ARGS) tests/


.PHONY: test
test: clean gen-extra-tests
	@echo "running tests"

	$(PYTHON) -m pytest $(PYTEST_OPTIONS) $(TESTS_DIR)


.PHONY: check
check: clean check-format test typing
	@echo "run format and lint checks, tests, and typing checks"

# build and publish
# ==================================================

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


# no zanj, it gets special treatment because it depends on muutils
# without urls since pytorch extra index breaks things
# no torch because we install it manually in CI
EXPORT_ARGS := -E array_no_torch -E notebook --with dev --with lint --without-hashes --without-urls

.PHONY: dep-dev
dep-dev:
	@echo "exporting dev and extras deps to $(REQ_DEV), lint/format deps to $(REQ_LINT)"
	poetry update
	poetry export $(EXPORT_ARGS) --output $(REQ_DEV)
	poetry export --only lint --without-hashes --without-urls --output $(REQ_LINT)

.PHONY: check-dep-dev
check-dep-dev:
	@echo "checking poetry lock is good, exported requirements match poetry"
	poetry check --lock
	poetry export $(EXPORT_ARGS) | diff - $(REQ_DEV)
	poetry export --only lint --without-hashes --without-urls | diff - $(REQ_LINT)

.PHONY: build
build: 
	@echo "build via poetry, assumes checks have been run"
	poetry build

.PHONY: publish
publish: gen-commit-log check build verify-git version gen-version-info
	@echo "run all checks, build, and then publish"

	@echo "Enter the new version number if you want to upload to pypi and create a new tag"
	@echo "Now would also be the time to edit $(COMMIT_LOG_FILE), as that will be used as the tag description"
	@read -p "Confirm: " NEW_VERSION; \
	if [ "$$NEW_VERSION" = $(VERSION) ]; then \
		echo "Version confirmed. Proceeding with publish."; \
	else \
		echo "Version mismatch, exiting: you gave $$NEW_VERSION but expected $(VERSION)"; \
		exit 1; \
	fi;

	@echo "pypi username: __token__"
	@echo "pypi token from '$(PYPI_TOKEN_FILE)' :"
	echo $$(cat $(PYPI_TOKEN_FILE))

	echo "Uploading!"; \
	echo $(VERSION) > $(LAST_VERSION_FILE); \
	git add $(LAST_VERSION_FILE); \
	git commit -m "Auto update to $(VERSION)"; \
	git tag -a $(VERSION) -F $(COMMIT_LOG_FILE); \
	git push origin $(VERSION); \
	twine upload dist/* --verbose

# cleanup
# ==================================================

.PHONY: clean
clean:
	@echo "cleaning up"
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf $(PACKAGE_NAME).egg-info
	rm -rf tests/junk_data
	$(PYTHON_BASE) -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	$(PYTHON_BASE) -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
	rm -rf tests/unit/validate_type/test_validate_type_GENERATED.py

# listing targets, from stackoverflow
# https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: help
help: gen-version-info
	@echo -n "list make targets"
	@echo ":"
	@cat Makefile | sed -n '/^\.PHONY: / h; /\(^\t@*echo\|^\t:\)/ {H; x; /PHONY/ s/.PHONY: \(.*\)\n.*"\(.*\)"/    make \1\t\2/p; d; x}'| sort -k2,2 |expand -t 25
	@echo "# makefile variables:"
	@echo "    PYTHON = $(PYTHON)"
	@echo "    PYTHON_VERSION = $(PYTHON_VERSION)"
	@echo "    PACKAGE_NAME = $(PACKAGE_NAME)"
	@echo "    VERSION = $(VERSION)"
	@echo "    LAST_VERSION = $(LAST_VERSION)"
	@echo "    PYTEST_OPTIONS = $(PYTEST_OPTIONS)"