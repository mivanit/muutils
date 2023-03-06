# python -m pylint muutils/
# python -m pylint tests/
lint:
	python -m mypy muutils/
	python -m pylint tests/

format:
	python -m black .

check-format:
	python -m black --check .

test:
	python -m pytest tests
