PACKAGE_NAME := muutils

PUBLISH_BRANCH := main
PYPI_TOKEN_FILE := .pypi-token
LAST_VERSION_FILE := .lastversion
COVERAGE_REPORTS_DIR := docs/coverage
TESTS_DIR := tests/unit
PYPROJECT := pyproject.toml

VERSION := $(shell python -c "import re; print(re.search(r'^version\s*=\s*\"(.+?)\"', open('$(PYPROJECT)').read(), re.MULTILINE).group(1))")
LAST_VERSION := $(shell cat $(LAST_VERSION_FILE))
PYTHON_BASE := python

# note that the commands at the end:
# 1) format the git log
# 2) replace backticks with single quotes, to avoid funny business
# 3) add a final newline, to make tac happy
# 4) reverse the order of the lines, so that the oldest commit is first
# 5) replace newlines with tabs, to prevent the newlines from being lost
COMMIT_LOG_FILE := .commit_log
COMMIT_LOG_SINCE_LAST_VERSION := $(shell (git log $(LAST_VERSION)..HEAD --pretty=format:"- %s (%h)" | tr '`' "'" ; echo) | tac | tr '\n' '\t')
#                                                                                    1                2            3       4     5

.PHONY: default
default: help

.PHONY: version
version:
	@echo "Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)"
	@echo "Commit log since last version:"
	@echo "$(COMMIT_LOG_SINCE_LAST_VERSION)" | tr '\t' '\n' > $(COMMIT_LOG_FILE)
	@cat $(COMMIT_LOG_FILE)
	@if [ "$(VERSION)" = "$(LAST_VERSION)" ]; then \
		echo "Python package $(VERSION) is the same as last published version $(LAST_VERSION), exiting!"; \
		exit 1; \
	fi

# command line options
# --------------------------------------------------
# for formatting or CI, we might want to run python without setting up all of poetry
RUN_GLOBAL ?= 0
ifeq ($(RUN_GLOBAL),0)
	PYTHON = poetry run $(PYTHON_BASE)
else
	PYTHON = $(PYTHON_BASE)
endif

PYTHON_VERSION := $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")

COMPATIBILITY_MODE := $(shell $(PYTHON) -c "import sys; print(1 if sys.version_info < (3, 10) else 0)")

TYPECHECK_ARGS ?= 

# formatting
# --------------------------------------------------

.PHONY: setup-format
setup-format:
	@echo "install only packages needed for formatting, direct via pip (useful for CI)"
	$(PYTHON_BASE) -c 'import re,tomllib; cfg = tomllib.load(open("$(PYPROJECT)", "rb")); deps = [(pkg, re.match(r"^\D*(\d.*)", ver).group(1)) for pkg, ver in cfg["tool"]["poetry"]["group"]["dev"]["dependencies"].items() if pkg in ["ruff", "pycln"]]; print(" ".join([f"{pkg}=={ver}" for pkg,ver in deps]))' | xargs $(PYTHON) -m pip install

.PHONY: format
format:
	@echo "format the source code"
	$(PYTHON) -m ruff format
	$(PYTHON) -m pycln --config $(PYPROJECT) --all .
	$(PYTHON) -m isort format .
	$(PYTHON) -m black .

.PHONY: check-format
check-format:
	@echo "run format check"
	$(PYTHON) -m ruff check
	$(PYTHON) -m pycln --check --config $(PYPROJECT) .
	$(PYTHON) -m isort --check-only .
	$(PYTHON) -m black --check .

# pytest options and coverage
# --------------------------------------------------

PYTEST_OPTIONS ?=

# whether to run pytest with coverage report generation
COV ?= 1

ifneq ($(COV), 0)
	PYTEST_OPTIONS += --cov=.
endif

# whether to run pytest with warnings as errors
WARN_STRICT ?= 0

ifneq ($(WARN_STRICT), 0)
    PYTEST_OPTIONS += -W error
endif

# compatibility mode for python <3.10

# Update the PYTEST_OPTIONS to include the conditional ignore option
ifeq ($(COMPATIBILITY_MODE), 1)
	JUNK := $(info WARNING: Detected python version less than 3.10, some behavior will be different)
    PYTEST_OPTIONS += --ignore=tests/unit/validate_type/
	TYPECHECK_ARGS += --disable-error-code misc --disable-error-code syntax --disable-error-code import-not-found
endif

.PHONY: cov
cov:
	@echo "generate coverage reports"
	$(PYTHON) -m coverage report -m > $(COVERAGE_REPORTS_DIR)/coverage.txt
	$(PYTHON) -m coverage_badge -f -o $(COVERAGE_REPORTS_DIR)/coverage.svg
	$(PYTHON) -m coverage html	

# tests
# --------------------------------------------------

# at some point, need to add back --check-untyped-defs to mypy call
# but it complains when we specify arguments by keyword where positional is fine
# not sure how to fix this
# python -m pylint $(PACKAGE_NAME)/
# python -m pylint tests/
.PHONY: typing
typing: clean
	@echo "running type checks"
	$(PYTHON) -m mypy --config-file $(PYPROJECT) $(TYPECHECK_ARGS) $(PACKAGE_NAME)/
	$(PYTHON) -m mypy --config-file $(PYPROJECT) $(TYPECHECK_ARGS) tests/


.PHONY: test
test: clean
	@echo "running tests"

	if [ $(COMPATIBILITY_MODE) -eq 0 ]; then \
		echo "converting certain tests to modern format"; \
		$(PYTHON) tests/util/replace_type_hints.py tests/unit/validate_type/test_validate_type.py > tests/unit/validate_type/test_validate_type_MODERN.py; \
	fi; \
	$(PYTHON) -m pytest $(PYTEST_OPTIONS) $(TESTS_DIR)


.PHONY: check
check: clean check-format clean test lint
	@echo "run format check, test, and lint"

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


# no zanj, it gets special treatment because it depends on muutils
# without urls since pytorch extra index breaks things
# no torch because we install it manually in CI
EXPORT_ARGS := -E array_no_torch -E notebook --with dev --without-hashes --without-urls

.PHONY: dep-dev
dep-dev:
	@echo "exporting dev and extras dependencies to dev-requirements.txt"
	poetry update
	poetry export $(EXPORT_ARGS) --output dev-requirements.txt

.PHONY: check-dep-dev
check-dep-dev:
	@echo "checking requirements.txt matches poetry dependencies"
	poetry check --lock
	poetry export $(EXPORT_ARGS) | diff - dev-requirements.txt

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
	git tag -a $(VERSION) -F $(COMMIT_LOG_FILE); \
	git push origin $(VERSION); \
	twine upload dist/* --verbose

# cleanup
# --------------------------------------------------

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
	rm -rf tests/unit/validate_type/test_validate_type_MODERN.py

# listing targets, from stackoverflow
# https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: help
help:
	@echo -n "# list make targets"
	@echo ":"
	@cat Makefile | sed -n '/^\.PHONY: / h; /\(^\t@*echo\|^\t:\)/ {H; x; /PHONY/ s/.PHONY: \(.*\)\n.*"\(.*\)"/    make \1\t\2/p; d; x}'| sort -k2,2 |expand -t 25
	@echo "# makefile variables:"
	@echo "    PYTHON = $(PYTHON)"
	@echo "    PYTHON_VERSION = $(PYTHON_VERSION)"
	@echo "    PACKAGE_NAME = $(PACKAGE_NAME)"
	@echo "    VERSION = $(VERSION)"
	@echo "    LAST_VERSION = $(LAST_VERSION)"
	@echo "    PYTEST_OPTIONS = $(PYTEST_OPTIONS)"