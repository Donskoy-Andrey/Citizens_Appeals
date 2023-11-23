## Install Python dependencies
install:
	@echo "$$(tput bold)Installing python dependencies...$$(tput sgr0)"
	pip install poetry
	poetry install
	poetry run pre-commit install

## Activate virtual environment
activate:
	@echo "$$(tput bold)Activating virtual environment...$$(tput sgr0)"
	poetry shell

## Setup project
setup: install activate

test:
	@echo "$$(tput bold)Running tests...$$(tput sgr0)"
	poetry run pytest tests/

## Run tests
tests: test

## Run script
run:
	@echo "$$(tput bold)Running script...$$(tput sgr0)"
	poetry run python project/source/main.py

## Clean cache files
clean:
	@echo "$$(tput bold)Cleaning cache files...$$(tput sgr0)"
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

runui:
	poetry run streamlit run project/source/web/ui.py
