# python -m pylint muutils/
# python -m pylint tests/
lint:
	python -m mypy --config-file pyproject.toml muutils/
	python -m pylint --config-file pyproject.toml tests/

lint-poetry:
	poetry run python --version
	poetry run python -m mypy --config-file pyproject.toml muutils/
	poetry run python -m pylint --config-file pyproject.toml tests/

lint-wip:
	python -m mypy muutils/
	python -m pylint tests/

format:
	python -m black .

check-format:
	python -m black --check .

test:
