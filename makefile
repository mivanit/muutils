# python -m pylint muutils/
# python -m pylint tests/
lint:
	rm -rf .mypy_cache
	python -m mypy --config-file pyproject.toml muutils/
	python -m mypy --config-file pyproject.toml tests/

format:
	python -m black .

check-format:
	python -m black --check .

test:
	echo "clearing cache"
	rm -rf .pytest_cache
	echo "clearing old data"
	rm -rf tests/junk_data
	echo "running tests"
	python -m pytest tests