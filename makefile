# python -m pylint muutils/
# python -m pylint tests/
lint:
	python -m mypy --config-file pyproject.toml muutils/
	python -m mypy --config-file pyproject.toml tests/

format:
	python -m black .

check-format:
	python -m black --check .

test:
