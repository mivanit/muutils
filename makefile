PACKAGE_NAME := muutils

PUBLISH_BRANCH := main
PYPI_TOKEN_FILE := .pypi-token
LAST_VERSION_FILE := .lastversion
COVERAGE_REPORTS_DIR := docs/coverage
TESTS_DIR := tests/unit
PYPROJECT := pyproject.toml

VERSION := $(shell python -c "import re; print(re.search(r'^version\s*=\s*\"(.+?)\"', open('$(PYPROJECT)').read(), re.MULTILINE).group(1))")
LAST_VERSION := $(shell cat $(LAST_VERSION_FILE))
PYPOETRY := poetry run python

# note that the commands at the end:
# 1) format the git log
# 2) replace backticks with single quotes, to avoid funny business
# 3) add a final newline, to make tac happy
# 4) reverse the order of the lines, so that the oldest commit is first
# 5) replace newlines with tabs, to prevent the newlines from being lost
COMMIT_LOG_FILE := .commit_log
COMMIT_LOG_SINCE_LAST_VERSION := $(shell (git log $(LAST_VERSION)..HEAD --pretty=format:"- %s (%h)" | tr '`' "'" ; echo) | tac | tr '\n' '\t')
#                                                                                    1                2            3       4     5

TYPECHECK_COMPAT_ARGS := --disable-error-code misc --disable-error-code syntax --disable-error-code import-not-found


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


# formatting
# --------------------------------------------------
.PHONY: format
format:
	python -m pycln --config $(PYPROJECT) --all .
	python -m isort format .
	python -m black .

.PHONY: check-format
check-format:
	@echo "run format check"
	python -m pycln --check --config $(PYPROJECT) .
	python -m isort --check-only .
	python -m black --check .

# coverage reports
# --------------------------------------------------
# whether to run pytest with coverage report generation
COV ?= 1

ifeq ($(COV),1)
    PYTEST_OPTIONS=--cov=.
else
    PYTEST_OPTIONS=
endif

.PHONY: cov
cov:
	@echo "generate coverage reports"
	$(PYPOETRY) -m coverage report -m > $(COVERAGE_REPORTS_DIR)/coverage.txt
	$(PYPOETRY) -m coverage_badge -f -o $(COVERAGE_REPORTS_DIR)/coverage.svg
	$(PYPOETRY) -m coverage html	

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
	$(PYPOETRY) -m mypy --config-file $(PYPROJECT) $(PACKAGE_NAME)/
	$(PYPOETRY) -m mypy --config-file $(PYPROJECT) tests/

.PHONY: typing-compat
typing-compat: clean
	@echo "running type checks in compatibility mode for older python versions"
	$(PYPOETRY) -m mypy --config-file $(PYPROJECT) $(TYPECHECK_COMPAT_ARGS) $(PACKAGE_NAME)/
	$(PYPOETRY) -m mypy --config-file $(PYPROJECT) $(TYPECHECK_COMPAT_ARGS) tests/

.PHONY: test
test: clean
	@echo "running tests"
	$(PYPOETRY) -m pytest $(PYTEST_OPTIONS) $(TESTS_DIR)


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