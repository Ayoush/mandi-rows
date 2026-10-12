.PHONY: dev test lint typecheck format clean

dev: install lint typecheck test

install:
	python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]"

test:
	. .venv/bin/activate && pytest -x -q

lint:
	. .venv/bin/activate && ruff check .

typecheck:
	. .venv/bin/activate && mypy src/

format:
	. .venv/bin/activate && ruff format .

clean:
	rm -rf .venv __pycache__ .pytest_cache .mypy_cache
