VERSION_INFO_LOCATION := muutils/__init__.py
PUBLISH_BRANCH := main
PYPI_TOKEN_FILE := .pypi-token
LAST_VERSION_FILE := .lastversion

VERSION := $(shell grep -oP '__version__ = "\K.*?(?=")' $(VERSION_INFO_LOCATION))
LAST_VERSION := $(shell cat $(LAST_VERSION_FILE))

.PHONY: default
default: help

.PHONY: version
version:
	@echo "Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)"
	@if [ "$(VERSION)" = "$(LAST_VERSION)" ]; then \
		echo "Python package $(VERSION) is the same as last published version $(LAST_VERSION), exiting!"; \
		exit 1; \
	fi

# python -m pylint muutils/
# python -m pylint tests/
.PHONY: lint
lint:
	rm -rf .mypy_cache
	python -m mypy --config-file pyproject.toml muutils/
	python -m mypy --config-file pyproject.toml tests/

.PHONY: format
format:
	python -m pycln --all .
	python -m isort format .
	python -m black .

.PHONY: check-format
check-format:
	@echo "run format check"
	python -m pycln --check --all .
	python -m isort --check-only .
	python -m black --check .

.PHONY: test
test:
	@echo "running tests"
	rm -rf .pytest_cache
	rm -rf tests/junk_data
	python -m pytest tests

.PHONY: check-git
check-git: 
	@echo "checking git status"
	if [ "$(shell git branch --show-current)" != $(PUBLISH_BRANCH) ]; then \
		echo "Git is not on the $(PUBLISH_BRANCH) branch, exiting!"; \
		exit 1; \
	fi; \
	if [ -n "$(shell git status --porcelain)" ]; then \
		echo "Git is not clean, exiting!"; \
		exit 1; \
	fi; \

#check-format test
.PHONY: build
build: 
	@echo "run format check, test, and then build"
	poetry build

.PHONY: publish
publish: check-format test build check-git version
	@echo "run format check, test, build, and then publish"

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

# workflow test -- no need to clear, runs using poetry
.PHONY: wftest
wftest:
	poetry run python -m pytest tests

.PHONY: wflint
wflint:
	poetry run python -m mypy --config-file pyproject.toml muutils/
	poetry run python -m mypy --config-file pyproject.toml tests/

# listing targets, from stackoverflow
# https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: help
help:
	@echo -n "# list make targets"
	@echo ":"
	@cat Makefile | sed -n '/^\.PHONY: / h; /\(^\t@*echo\|^\t:\)/ {H; x; /PHONY/ s/.PHONY: \(.*\)\n.*"\(.*\)"/    make \1\t\2/p; d; x}'| sort -k2,2 |expand -t 25