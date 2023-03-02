test:
	poetry run python -m pytest tests

format:
	poetry run python -m pycln --config pyproject.toml .
	poetry run python -m isort format .
	poetry run python -m black .

check-format:
	poetry run python -m pycln --check --config pyproject.toml .
	poetry run python -m isort --check-only .
	poetry run python -m black --check .
