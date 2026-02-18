#|==================================================================|
#| python project makefile template                                 |
#| originally by Michael Ivanitskiy (mivanits@umich.edu)            |
#| https://github.com/mivanit/python-project-makefile-template      |
#| version: v0.5.1                                                  |
#| license: https://creativecommons.org/licenses/by-sa/4.0/         |
#|==================================================================|
#| CUSTOMIZATION:                                                   |
#| - modify PACKAGE_NAME and other variables in config section      |
#| - mark custom changes with `~~~~~` for easier template updates   |
#| - run `make help` to see available targets                       |
#| - run `make help=TARGET` for detailed info about specific target |
#|==================================================================|


 ######  ########  ######
##    ## ##       ##    ##
##       ##       ##
##       ######   ##   ####
##       ##       ##    ##
##    ## ##       ##    ##
 ######  ##        ######

# ==================================================
# configuration & variables
# ==================================================


# !!! MODIFY AT LEAST THIS PART TO SUIT YOUR PROJECT !!!
# it assumes that the source is in a directory named the same as the package name
# this also gets passed to some other places
PACKAGE_NAME := muutils

# for checking you are on the right branch when publishing
PUBLISH_BRANCH := main

# where to put docs
# if you change this, you must also change pyproject.toml:tool.makefile.docs.output_dir to match
DOCS_DIR := docs

# where the tests are, for pytest
TESTS_DIR := tests

# tests temp directory to clean up. will remove this in `make clean`
TESTS_TEMP_DIR := $(TESTS_DIR)/_temp/

# probably don't change these:
# --------------------------------------------------

# where the pyproject.toml file is. no idea why you would change this but just in case
PYPROJECT := pyproject.toml

# name of this makefile -- change if you rename it to `Makefile` or similar
MAKEFILE_NAME := makefile

# dir to store various configuration files
# use of `.meta/` inspired by https://news.ycombinator.com/item?id=36472613
META_DIR := .meta

# scripts download configuration
# override SCRIPTS_VERSION to download a specific version (e.g., make self-setup-scripts SCRIPTS_VERSION=v0.5.0)
SCRIPTS_DIR := $(META_DIR)/scripts
SCRIPTS_VERSION ?= main
SCRIPTS_REPO := mivanit/python-project-makefile-template
SCRIPTS_URL_BASE := https://raw.githubusercontent.com/$(SCRIPTS_REPO)/$(SCRIPTS_VERSION)/scripts/out

# requirements.txt files for base package, all extras, dev, and all
REQUIREMENTS_DIR := $(META_DIR)/requirements

# local files (don't push this to git!)
LOCAL_DIR := $(META_DIR)/local

# will print this token when publishing. make sure not to commit this file!!!
PYPI_TOKEN_FILE := $(LOCAL_DIR)/.pypi-token

# version files
VERSIONS_DIR := $(META_DIR)/versions

# the last version that was auto-uploaded. will use this to create a commit log for version tag
# see `gen-commit-log` target
LAST_VERSION_FILE := $(VERSIONS_DIR)/.lastversion

# current version (writing to file needed due to shell escaping issues)
VERSION_FILE := $(VERSIONS_DIR)/.version

# base python to use. Will add `uv run` in front of this if `RUN_GLOBAL` is not set to 1
PYTHON_BASE := python

# where the commit log will be stored
COMMIT_LOG_FILE := $(LOCAL_DIR)/.commit_log

# where to put the coverage reports
# note that this will be published with the docs!
# modify the `docs` targets and `.gitignore` if you don't want that
COVERAGE_REPORTS_DIR := $(DOCS_DIR)/coverage

# this stuff in the docs will be kept
# in addition to anything specified in `pyproject.toml:tool.makefile.docs.no_clean`
DOCS_RESOURCES_DIR := $(DOCS_DIR)/resources

# location of the make docs script
MAKE_DOCS_SCRIPT_PATH := $(SCRIPTS_DIR)/make_docs.py

# options to pass to `uv sync` when syncing dependencies. by default, syncs all extras and groups (including dev dependencies)
# `--compile-bytecode` is added when running `make dep-compile`
UV_SYNC_OPTIONS := --all-extras --all-groups

# version vars - extracted automatically from `pyproject.toml`, `$(LAST_VERSION_FILE)`, and $(PYTHON)
# --------------------------------------------------

# assuming your `pyproject.toml` has a line that looks like `version = "0.0.1"`, `gen-version-info` will extract this
PROJ_VERSION := NULL
# `gen-version-info` will read the last version from `$(LAST_VERSION_FILE)`, or `NULL` if it doesn't exist
LAST_VERSION := NULL
# get the python version, now that we have picked the python command
PYTHON_VERSION := NULL

# type checker configuration
# --------------------------------------------------

# which type checkers to run (comma-separated)
# available: ty,basedpyright,mypy
TYPE_CHECKERS ?= ty,basedpyright,mypy

# path to type check (empty = use config from pyproject.toml)
TYPECHECK_PATH ?=

# directory to store type checker outputs
TYPE_ERRORS_DIR := $(META_DIR)/.type-errors

# typing summary output file
TYPING_SUMMARY_FILE := $(META_DIR)/typing-summary.toml


# ==================================================
# reading command line options
# ==================================================


# for formatting or something, we might want to run python without uv
# RUN_GLOBAL=1 to use global `PYTHON_BASE` instead of `uv run $(PYTHON_BASE)`
RUN_GLOBAL ?= 0

# for running tests or other commands without updating the env, set this to 1
# and it will pass `--no-sync` to `uv run`
UV_NOSYNC ?= 0

ifeq ($(RUN_GLOBAL),0)
	ifeq ($(UV_NOSYNC),1)
		PYTHON = uv run --no-sync $(PYTHON_BASE)
	else
		PYTHON = uv run $(PYTHON_BASE)
	endif
else
	PYTHON = $(PYTHON_BASE)
endif

# if you want different behavior for different python versions
# --------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# compatibility mode for python <3.10
# loose typing, allow warnings for python <3.10

TYPECHECK_ARGS ?=

# COMPATIBILITY_MODE: whether to run in compatibility mode for python <3.11
COMPATIBILITY_MODE := $(shell $(PYTHON) -c "import sys; print(1 if sys.version_info < (3, 11) else 0)")

ifeq ($(COMPATIBILITY_MODE), 1)
	JUNK := $(info !!! WARNING !!!: Detected python version less than 3.11, some behavior will be different)
	TYPECHECK_ARGS += --disable-error-code misc --disable-error-code syntax --disable-error-code import-not-found --no-check-untyped-defs
endif
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# options we might want to pass to pytest
# --------------------------------------------------

# base options for pytest, user can set this when running make to add more options
PYTEST_OPTIONS ?=


# ==================================================
# default target (help)
# ==================================================


# first/default target is help
.PHONY: default
default: help



 ######   ######  ########  #### ########  ########  ######
##    ## ##    ## ##     ##  ##  ##     ##    ##    ##    ##
##       ##       ##     ##  ##  ##     ##    ##    ##
 ######  ##       ########   ##  ########     ##     ######
      ## ##       ##   ##    ##  ##           ##          ##
##    ## ##    ## ##    ##   ##  ##           ##    ##    ##
 ######   ######  ##     ## #### ##           ##     ######

# ==================================================
# downloading scripts from github
# ==================================================

# list of scripts to download when running `make self-setup-scripts`. these are the helper scripts that the makefile uses for various tasks (e.g., getting version info, generating docs, etc.)
SCRIPTS_LIST := export_requirements get_version get_commit_log check_torch get_todos pdoc_markdown2_cli docs_clean typing_breakdown recipe_info make_docs generate_badge

# download makefile helper scripts from GitHub
# uses curl to fetch scripts from the template repository
# override version: make self-setup-scripts SCRIPTS_VERSION=v0.5.0
.PHONY: self-setup-scripts
self-setup-scripts:
	@echo "downloading makefile scripts (version: $(SCRIPTS_VERSION))"
	@mkdir -p $(SCRIPTS_DIR)
	@for script in $(SCRIPTS_LIST); do \
		echo "  $$script.py"; \
		curl -fsSL "$(SCRIPTS_URL_BASE)/$$script.py" -o "$(SCRIPTS_DIR)/$$script.py"; \
	done
	@echo "$(SCRIPTS_VERSION)" > $(SCRIPTS_DIR)/VERSION
	@echo "done"

##     ## ######## ########   ######  ####  #######  ##    ##
##     ## ##       ##     ## ##    ##  ##  ##     ## ###   ##
##     ## ##       ##     ## ##        ##  ##     ## ####  ##
##     ## ######   ########   ######   ##  ##     ## ## ## ##
 ##   ##  ##       ##   ##         ##  ##  ##     ## ##  ####
  ## ##   ##       ##    ##  ##    ##  ##  ##     ## ##   ###
   ###    ######## ##     ##  ######  ####  #######  ##    ##

# ==================================================
# getting version info
# we do this in a separate target because it takes a bit of time
# ==================================================


# this recipe is weird. we need it because:
# - a one liner for getting the version with toml is unwieldy, and using regex is fragile
# - using $$SCRIPT_GET_VERSION within $(shell ...) doesn't work because of escaping issues
# - trying to write to the file inside the `gen-version-info` recipe doesn't work, 
#   shell eval happens before our `python ...` gets run and `cat` doesn't see the new file
.PHONY: write-proj-version
write-proj-version:
	@mkdir -p $(VERSIONS_DIR)
	@$(PYTHON) $(SCRIPTS_DIR)/get_version.py "$(PYPROJECT)" > $(VERSION_FILE)

# gets version info from $(PYPROJECT), last version from $(LAST_VERSION_FILE), and python version
# uses just `python` for everything except getting the python version. no echo here, because this is "private"
.PHONY: gen-version-info
gen-version-info: write-proj-version
	@mkdir -p $(LOCAL_DIR)
	$(eval PROJ_VERSION := $(shell cat $(VERSION_FILE)) )
	$(eval LAST_VERSION := $(shell [ -f $(LAST_VERSION_FILE) ] && cat $(LAST_VERSION_FILE) || echo NULL) )
	$(eval PYTHON_VERSION := $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')") )

# getting commit log since the tag specified in $(LAST_VERSION_FILE)
# will write to $(COMMIT_LOG_FILE)
# when publishing, the contents of $(COMMIT_LOG_FILE) will be used as the tag description (but can be edited during the process)
# no echo here, because this is "private"
.PHONY: gen-commit-log
gen-commit-log: gen-version-info
	@if [ "$(LAST_VERSION)" = "NULL" ]; then \
		echo "!!! ERROR !!!"; \
		echo "LAST_VERSION is NULL, cant get commit log!"; \
		exit 1; \
	fi
	@mkdir -p $(LOCAL_DIR)
	@$(PYTHON) $(SCRIPTS_DIR)/get_commit_log.py "$(LAST_VERSION)" "$(COMMIT_LOG_FILE)"


# force the version info to be read, printing it out
# also force the commit log to be generated, and cat it out
.PHONY: version
version: gen-commit-log
	@echo "Current version is $(PROJ_VERSION), last auto-uploaded version is $(LAST_VERSION)"
	@echo "Commit log since last version from '$(COMMIT_LOG_FILE)':"
	@cat $(COMMIT_LOG_FILE)
	@echo ""
	@if [ "$(PROJ_VERSION)" = "$(LAST_VERSION)" ]; then \
		echo "!!! ERROR !!!"; \
		echo "Python package $(PROJ_VERSION) is the same as last published version $(LAST_VERSION), exiting!"; \
		exit 1; \
	fi



########  ######## ########   ######
##     ## ##       ##     ## ##    ##
##     ## ##       ##     ## ##
##     ## ######   ########   ######
##     ## ##       ##              ##
##     ## ##       ##        ##    ##
########  ######## ##         ######

# ==================================================
# dependencies and setup
# ==================================================


.PHONY: setup
setup: self-setup-scripts dep-check
	@echo "download scripts and sync dependencies"
	@echo ""
	@echo "setup complete! To activate the virtual environment, run one of:"
	@echo "  source .venv/bin/activate"
	@echo "  source .venv/Scripts/activate"

.PHONY: dep-check-torch
dep-check-torch:
	@echo "see if torch is installed, and which CUDA version and devices it sees"
	$(PYTHON) $(SCRIPTS_DIR)/check_torch.py

# sync dependencies and export to requirements.txt files
# - syncs all extras and groups with uv (including dev dependencies)
# - compiles bytecode for faster imports
# - exports to requirements.txt files per tool.uv-exports.exports config
# configure via pyproject.toml:[tool.uv-exports]:
#   [tool.uv-exports]
#   exports = [
#     { name = "base", extras = [], groups = [] },  # base package deps only
#     { name = "dev", extras = [], groups = ["dev"] },  # dev dependencies
#     { name = "all", extras = ["all"], groups = ["dev"] }  # everything
#   ]
.PHONY: dep
dep:
	@echo "syncing and exporting dependencies as per $(PYPROJECT) section 'tool.uv-exports.exports'"
	uv sync $(UV_SYNC_OPTIONS)
	mkdir -p $(REQUIREMENTS_DIR)
	$(PYTHON) $(SCRIPTS_DIR)/export_requirements.py $(PYPROJECT) $(REQUIREMENTS_DIR) | sh -x

.PHONY: dep-compile
dep-compile:
	@echo "syncing dependencies with bytecode compilation"
	$(MAKE) dep UV_SYNC_OPTIONS="$(UV_SYNC_OPTIONS) --compile-bytecode"


# verify that requirements.txt files match current dependencies
# - exports deps to temp directory
# - diffs temp against existing requirements files
# - FAILS if any differences found (means you need to run `make dep`)
# useful in CI to catch when pyproject.toml changed but requirements weren't regenerated
.PHONY: dep-check
dep-check:
	@echo "Checking that exported requirements are up to date"
	uv sync --all-extras --all-groups
	mkdir -p $(REQUIREMENTS_DIR)-TEMP
	$(PYTHON) $(SCRIPTS_DIR)/export_requirements.py $(PYPROJECT) $(REQUIREMENTS_DIR)-TEMP | sh -x
	diff -r $(REQUIREMENTS_DIR)-TEMP $(REQUIREMENTS_DIR)
	rm -rf $(REQUIREMENTS_DIR)-TEMP


.PHONY: dep-clean
dep-clean:
	@echo "clean up lock files, .venv, and requirements files"
	rm -rf .venv
	rm -rf uv.lock
	rm -rf $(REQUIREMENTS_DIR)/*.txt


 ######  ##     ## ########  ######  ##    ##  ######
##    ## ##     ## ##       ##    ## ##   ##  ##    ##
##       ##     ## ##       ##       ##  ##   ##
##       ######### ######   ##       #####     ######
##       ##     ## ##       ##       ##  ##         ##
##    ## ##     ## ##       ##    ## ##   ##  ##    ##
 ######  ##     ## ########  ######  ##    ##  ######

# ==================================================
# checks (formatting/linting, typing, tests)
# ==================================================


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# added gen-extra-tests and it is required by some other recipes:
# typing, typing-summary, test

# extra tests with python >=3.10 type hints
.PHONY: gen-extra-tests
gen-extra-tests:
	@COMPAT=$$($(PYTHON) -c "import sys; print(1 if sys.version_info < (3, 10) else 0)"); \
	if [ "$$COMPAT" -eq 0 ]; then \
		echo "converting certain tests to modern format"; \
		$(PYTHON) tests/util/replace_type_hints.py tests/unit/validate_type/test_validate_type.py "# DO NOT EDIT, GENERATED FILE" > tests/unit/validate_type/test_validate_type_GENERATED.py; \
	fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# format code AND auto-fix linting issues
# performs TWO operations: reformats code, then auto-fixes safe linting issues
# configure in pyproject.toml:[tool.ruff]
.PHONY: format
format:
	@echo "format the source code"
	$(PYTHON) -m ruff format --config $(PYPROJECT) .
	$(PYTHON) -m ruff check --fix --config $(PYPROJECT) .

# runs ruff to check if the code is formatted correctly
.PHONY: format-check
format-check:
	@echo "check if the source code is formatted correctly"
	$(PYTHON) -m ruff check --config $(PYPROJECT) .

# runs type checks with configured checkers
# set TYPE_CHECKERS to customize which checkers run (e.g., TYPE_CHECKERS=mypy,basedpyright)
# set TYPING_OUTPUT_DIR to save outputs to files (used by typing-summary)
# returns exit code 1 if any checker fails
.PHONY: typing
typing: gen-extra-tests
	@echo "running type checks"
	@div="--------------------------------------------------"; \
	failed=0; \
	for c in $$(echo "$(TYPE_CHECKERS)" | tr ',' ' '); do \
		case "$$c" in ty) subcmd="check";; *) subcmd="";; esac; \
		printf "\033[36m$$div\n[$$c]\n$$div\033[0m\n"; \
		$(PYTHON) -m $$c $$subcmd $(TYPECHECK_ARGS) $(TYPECHECK_PATH) $(if $(TYPING_OUTPUT_DIR),> $(TYPING_OUTPUT_DIR)/$$c.txt 2>&1) || failed=1; \
	done; \
	if [ $$failed -eq 1 ]; then \
		printf "\033[31m$$div\nnot all type checks passed\n$$div\033[0m\n"; \
		exit 1; \
	else \
		printf "\033[32m$$div\nall type checks passed\n$$div\033[0m\n"; \
	fi

# save type check outputs and generate detailed breakdown
# outputs are saved to $(TYPE_ERRORS_DIR)/*.txt
# summary is generated to $(TYPING_SUMMARY_FILE)
.PHONY: typing-summary
typing-summary: gen-extra-tests
	@echo "running type checks and saving to $(TYPE_ERRORS_DIR)/"
	@mkdir -p $(TYPE_ERRORS_DIR)
	-@$(MAKE) --no-print-directory typing TYPING_OUTPUT_DIR=$(TYPE_ERRORS_DIR)
	@echo "generating typing summary..."
	$(PYTHON) $(SCRIPTS_DIR)/typing_breakdown.py --error-dir $(TYPE_ERRORS_DIR) --output $(TYPING_SUMMARY_FILE) --checkers $(TYPE_CHECKERS)

# run tests with pytest
# you can pass custom args. for example:
# make test PYTEST_OPTIONS="--maxfail=1 -x"
# pytest config in pyproject.toml:[tool.pytest.ini_options]
.PHONY: test
test: gen-extra-tests
	@echo "running tests"
	$(PYTHON) -m pytest $(PYTEST_OPTIONS) $(TESTS_DIR)

.PHONY: check
check: format-check test typing
	@echo "run format checks, tests, and typing checks"


########   #######   ######   ######
##     ## ##     ## ##    ## ##    ##
##     ## ##     ## ##       ##
##     ## ##     ## ##        ######
##     ## ##     ## ##             ##
##     ## ##     ## ##    ## ##    ##
########   #######   ######   ######

# ==================================================
# coverage & docs
# ==================================================


# generates a whole tree of documentation in html format.
# see `$(MAKE_DOCS_SCRIPT_PATH)` and the templates in `$(DOCS_RESOURCES_DIR)/templates/html/` for more info
.PHONY: docs-html
docs-html:
	@echo "generate html docs"
	$(PYTHON) $(MAKE_DOCS_SCRIPT_PATH)

# instead of a whole website, generates a single markdown file with all docs using the templates in `$(DOCS_RESOURCES_DIR)/templates/markdown/`.
# this is useful if you want to have a copy that you can grep/search, but those docs are much messier.
.PHONY: docs-md
docs-md:
	@echo "generate combined (single-file) docs in markdown"
	mkdir $(DOCS_DIR)/combined -p
	$(PYTHON) $(MAKE_DOCS_SCRIPT_PATH) --combined

# generate coverage reports from test results
# WARNING: if .coverage file not found, will automatically run `make test` first
# - generates text report: $(COVERAGE_REPORTS_DIR)/coverage.txt
# - generates SVG badge: $(COVERAGE_REPORTS_DIR)/coverage.svg
# - generates HTML report: $(COVERAGE_REPORTS_DIR)/html/
# - removes .gitignore from html dir (we publish coverage with docs)
.PHONY: cov
cov:
	@echo "generate coverage reports"
	@if [ ! -f .coverage ]; then \
		echo ".coverage not found, running tests first..."; \
		$(MAKE) test PYTEST_OPTIONS="$(PYTEST_OPTIONS) --cov=." ; \
	fi
	mkdir $(COVERAGE_REPORTS_DIR) -p
	$(PYTHON) -m coverage report -m > $(COVERAGE_REPORTS_DIR)/coverage.txt
	$(PYTHON) $(SCRIPTS_DIR)/generate_badge.py --coverage $(COVERAGE_REPORTS_DIR)/coverage.txt > $(COVERAGE_REPORTS_DIR)/coverage.svg
	$(PYTHON) -m coverage html --directory=$(COVERAGE_REPORTS_DIR)/html/
	rm -rf $(COVERAGE_REPORTS_DIR)/html/.gitignore

# runs the coverage report, then the docs, then the combined docs
.PHONY: docs
docs: cov docs-html docs-md todo lmcat
	@echo "generate all documentation and coverage reports"

# remove generated documentation files, but preserve resources
# - removes all docs except those in DOCS_RESOURCES_DIR
# - preserves files/patterns specified in pyproject.toml config
# - distinct from `make clean` (which removes temp build files, not docs)
# configure via pyproject.toml:[tool.makefile.docs]:
#   [tool.makefile.docs]
#   output_dir = "docs"  # must match DOCS_DIR in makefile
#   no_clean = [  # files/patterns to preserve when cleaning
#     "resources/**",
#     "*.svg",
#     "*.css"
#   ]
.PHONY: docs-clean
docs-clean:
	@echo "remove generated docs except resources"
	$(PYTHON) $(SCRIPTS_DIR)/docs_clean.py $(PYPROJECT) $(DOCS_DIR) $(DOCS_RESOURCES_DIR)


# get all TODO's from the code
# configure via pyproject.toml:[tool.makefile.inline-todo]:
#   [tool.makefile.inline-todo]
#   search_dir = "."  # directory to search for TODOs
#   out_file_base = "docs/other/todo-inline"  # output file path (without extension)
#   context_lines = 2  # lines of context around each TODO
#   extensions = ["py", "md"]  # file extensions to search
#   tags = ["CRIT", "TODO", "FIXME", "HACK", "BUG", "DOC"]  # tags to look for
#   exclude = ["docs/**", ".venv/**", "scripts/get_todos.py"]  # patterns to exclude
#   branch = "main"  # git branch for URLs
#   # repo_url = "..."  # repository URL (defaults to [project.urls.{repository,github}])
#   # template_md = "..."  # custom jinja2 template for markdown output
#   # template_issue = "..."  # custom format string for issues
#   # template_html_source = "..."  # custom html template path
#   tag_label_map = { "BUG" = "bug", "TODO" = "enhancement", "DOC" = "documentation" } # mapping of tags to GitHub issue labels
.PHONY: todo
todo:
	@echo "get all TODO's from the code"
	$(PYTHON) $(SCRIPTS_DIR)/get_todos.py

.PHONY: lmcat-tree
lmcat-tree:
	@echo "show in console the lmcat tree view"
	-$(PYTHON) -m lmcat -t --output STDOUT

.PHONY: lmcat
lmcat:
	@echo "write the lmcat full output to pyproject.toml:[tool.lmcat.output]"
	-$(PYTHON) -m lmcat

########  ##     ## #### ##       ########
##     ## ##     ##  ##  ##       ##     ##
##     ## ##     ##  ##  ##       ##     ##
########  ##     ##  ##  ##       ##     ##
##     ## ##     ##  ##  ##       ##     ##
##     ## ##     ##  ##  ##       ##     ##
########   #######  #### ######## ########

# ==================================================
# build and publish
# ==================================================


# verify git is ready for publishing
# REQUIRES:
# - current branch must be $(PUBLISH_BRANCH)
# - no uncommitted changes (git status --porcelain must be empty)
# EXITS with error if either condition fails
.PHONY: verify-git
verify-git:
	@echo "checking git status"
	if [ "$(shell git branch --show-current)" != $(PUBLISH_BRANCH) ]; then \
		echo "!!! ERROR !!!"; \
		echo "Git is not on the $(PUBLISH_BRANCH) branch, exiting!"; \
		git branch; \
		git status; \
		exit 1; \
	fi; \
	if [ -n "$(shell git status --porcelain)" ]; then \
		echo "!!! ERROR !!!"; \
		echo "Git is not clean, exiting!"; \
		git status; \
		exit 1; \
	fi; \


# build package distribution files
# creates wheel (.whl) and source distribution (.tar.gz) in dist/
.PHONY: build
build:
	@echo "build the package"
	uv build

# publish package to PyPI and create git tag
# PREREQUISITES:
# - must be on $(PUBLISH_BRANCH) branch with clean git status (verified by verify-git)
# - must have $(PYPI_TOKEN_FILE) with your PyPI token
# - version in pyproject.toml must be different from $(LAST_VERSION_FILE)
# PROCESS:
# 1. runs checks, validates version, builds package, verifies git clean
# 2. prompts for version confirmation (you can edit $(COMMIT_LOG_FILE) at this point)
# 3. creates git commit updating $(LAST_VERSION_FILE)
# 4. creates annotated git tag with commit log as description
# 5. pushes tag to origin
# 6. uploads to PyPI via twine
.PHONY: publish
publish: check version build verify-git
	@echo "Ready to publish $(PROJ_VERSION) to PyPI"
	@echo "Now would be the time to edit $(COMMIT_LOG_FILE) for the tag description"

	@read -p "Enter version to confirm: " NEW_VERSION && \
	if [ "$$NEW_VERSION" != "$(PROJ_VERSION)" ]; then \
		echo "Version mismatch: got $$NEW_VERSION, expected $(PROJ_VERSION)"; \
		exit 1; \
	fi && \
	echo "Version confirmed."

	@test -f "$(PYPI_TOKEN_FILE)" || { echo "ERROR: Token file not found at $(PYPI_TOKEN_FILE)"; exit 1; }

	@echo "Committing and tagging..."
	echo $(PROJ_VERSION) > $(LAST_VERSION_FILE) && \
	git add $(LAST_VERSION_FILE) && \
	git commit -m "Auto update to $(PROJ_VERSION)" && \
	git tag -a $(PROJ_VERSION) -F $(COMMIT_LOG_FILE) && \
	git push origin $(PROJ_VERSION)

	@echo "Uploading to PyPI..."
	TWINE_USERNAME=__token__ TWINE_PASSWORD="$$(cat $(PYPI_TOKEN_FILE))" $(PYTHON) -m twine upload dist/* --verbose

	@echo "Published $(PROJ_VERSION) successfully!"

# ==================================================
# cleanup of temp files
# ==================================================


# cleans up temporary files:
# - caches: .mypy_cache, .ruff_cache, .pytest_cache, .coverage
# - build artifacts: dist/, build/, *.egg-info
# - test temp files: $(TESTS_TEMP_DIR)
# - __pycache__ directories and *.pyc/*.pyo files in $(PACKAGE_NAME), $(TESTS_DIR), $(DOCS_DIR)
# uses `-` prefix on find commands to continue even if directories don't exist
# distinct from `make docs-clean`, which removes generated documentation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# added cleanup of generated test file
.PHONY: clean
clean:
	@echo "clean up temporary files"
	rm -rf .mypy_cache .ruff_cache .pytest_cache .coverage dist build $(PACKAGE_NAME).egg-info $(TESTS_TEMP_DIR) $(TYPE_ERRORS_DIR)
	-find $(PACKAGE_NAME) $(TESTS_DIR) $(DOCS_DIR) -type d -name '__pycache__' -exec rm -rf {} +
	-find $(PACKAGE_NAME) $(TESTS_DIR) $(DOCS_DIR) -type f -name '*.py[co]' -delete
	rm -f tests/unit/validate_type/test_validate_type_GENERATED.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# remove all generated/build files including .venv
# runs: clean + docs-clean + dep-clean
# removes .venv, uv.lock, requirements.txt files, generated docs, build artifacts
# run `make dep` after this to reinstall dependencies
.PHONY: clean-all
clean-all: clean docs-clean dep-clean
	@echo "clean up all temporary files, dep files, venv, and generated docs"


##     ## ######## ##       ########
##     ## ##       ##       ##     ##
##     ## ##       ##       ##     ##
######### ######   ##       ########
##     ## ##       ##       ##
##     ## ##       ##       ##
##     ## ######## ######## ##

# ==================================================
# smart help command
# ==================================================


# listing targets is from stackoverflow
# https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
# no .PHONY because this will only be run before `make help`
# it's a separate command because getting the `info` takes a bit of time
# and we want to show the make targets right away without making the user wait for `info` to finish running
help-targets:
	@echo -n "# make targets"
	@echo ":"
	@cat $(MAKEFILE_NAME) | sed -n '/^\.PHONY: / h; /\(^\t@*echo\|^\t:\)/ {H; x; /PHONY/ s/.PHONY: \(.*\)\n.*"\(.*\)"/    make \1\t\2/p; d; x}'| sort -k2,2 |expand -t 30


.PHONY: info
info: gen-version-info
	@echo "# makefile variables"
	@echo "    PYTHON = $(PYTHON)"
	@echo "    PYTHON_VERSION = $(PYTHON_VERSION)"
	@echo "    PACKAGE_NAME = $(PACKAGE_NAME)"
	@echo "    PROJ_VERSION = $(PROJ_VERSION)"
	@echo "    LAST_VERSION = $(LAST_VERSION)"
	@echo "    PYTEST_OPTIONS = $(PYTEST_OPTIONS)"

.PHONY: info-long
info-long: info
	@echo "# other variables"
	@echo "    PUBLISH_BRANCH = $(PUBLISH_BRANCH)"
	@echo "    DOCS_DIR = $(DOCS_DIR)"
	@echo "    COVERAGE_REPORTS_DIR = $(COVERAGE_REPORTS_DIR)"
	@echo "    TESTS_DIR = $(TESTS_DIR)"
	@echo "    TESTS_TEMP_DIR = $(TESTS_TEMP_DIR)"
	@echo "    PYPROJECT = $(PYPROJECT)"
	@echo "    REQUIREMENTS_DIR = $(REQUIREMENTS_DIR)"
	@echo "    LOCAL_DIR = $(LOCAL_DIR)"
	@echo "    PYPI_TOKEN_FILE = $(PYPI_TOKEN_FILE)"
	@echo "    LAST_VERSION_FILE = $(LAST_VERSION_FILE)"
	@echo "    PYTHON_BASE = $(PYTHON_BASE)"
	@echo "    COMMIT_LOG_FILE = $(COMMIT_LOG_FILE)"
	@echo "    RUN_GLOBAL = $(RUN_GLOBAL)"
	@echo "    TYPECHECK_ARGS = $(TYPECHECK_ARGS)"
	@echo "    TYPECHECK_PATH = $(TYPECHECK_PATH)"
	@echo "    TYPE_CHECKERS = $(TYPE_CHECKERS)"
	@echo "    COMPATIBILITY_MODE = $(COMPATIBILITY_MODE)"

# Smart help command: shows general help, or detailed info about specific targets
# Usage:
#   make help              - shows general help (list of targets + makefile variables)
#   make help="test"       - shows detailed info about the 'test' recipe
#   make HELP="test clean" - shows detailed info about multiple recipes
#   make h=*               - shows detailed info about all recipes (wildcard expansion)
#   make H="test"          - same as HELP (case variations supported)
#
# All variations work: help/HELP/h/H with values like "foo", "foo bar", "*", "--all"
.PHONY: help
help:
	@$(eval HELP_ARG := $(or $(HELP),$(help),$(H),$(h)))
	@$(eval HELP_EXPANDED := $(if $(filter *,$(HELP_ARG)),--all,$(HELP_ARG)))
	@if [ -n "$(HELP_EXPANDED)" ]; then \
		$(PYTHON_BASE) $(SCRIPTS_DIR)/recipe_info.py -f $(MAKEFILE_NAME) "$(HELP_EXPANDED)"; \
	else \
		$(MAKE) --no-print-directory help-targets info; \
		echo ""; \
		echo "To get detailed info about specific make targets or variables, use:"; \
		echo "  make help=TARGET    or    make HELP=\"TARGET1 TARGET2\""; \
		echo "  make help=VARIABLE  - shows variable values (case-insensitive)"; \
		echo "  make H=*            or    make h=--all"; \
	fi


 ######  ##     ##  ######  ########  #######  ##     ##
##    ## ##     ## ##    ##    ##    ##     ## ###   ###
##       ##     ## ##          ##    ##     ## #### ####
##       ##     ##  ######     ##    ##     ## ## ### ##
##       ##     ##       ##    ##    ##     ## ##     ##
##    ## ##     ## ##    ##    ##    ##     ## ##     ##
 ######   #######   ######     ##     #######  ##     ##

# ==================================================
# custom targets
# ==================================================
# (put them down here, or delimit with ~~~~~)