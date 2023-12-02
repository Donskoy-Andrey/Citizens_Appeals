## Install Python dependencies
install:
	@echo "Installing python dependencies..."
	python3 -m pip install poetry
	python3 -m spacy download ru_core_news_sm
	poetry install
	poetry run pre-commit install

## Activate virtual environment
activate:
	@echo "Activating virtual environment..."
	poetry shell

## Migration
migration:
	@echo "Make migrations..."
	poetry run python project/source/manage.py makemigrations --merge
	poetry run python project/source/manage.py migrate

## Setup project
setup: install activate migration

test:
	@echo "Running tests..."
	poetry run pytest tests/

## Run tests
tests: test

## Clean cache files
clean:
	@echo "Cleaning cache files..."
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache

## Show help
help:
	@echo "$$(tput bold)Available commands:$$(tput sgr0)"
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')

run_windows:
	poetry run python .\project\source\manage.py runserver

run_linux:
	poetry run python project/source/manage.py runserver
