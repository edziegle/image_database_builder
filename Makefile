.PHONY: test clean clean-logs clean-database run-sample

clean: clean-database clean-logs

clean-logs: logs
	rm -rf logs/*

clean-database: image-database.db
	rm image-database.db

test:
	poetry run pytest

run-sample: clean
	poetry run python src/builder.py bin/sampleindex

format:
	poetry run black src tests
	poetry run isort src tests

lint:
	poetry run flake8 src tests --max-line-length=120
	poetry run black --check src tests
	poetry run isort --check-only src tests

prepare-for-pr: format lint test