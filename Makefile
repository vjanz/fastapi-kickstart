.PHONY: format lint help test up down down-v migrate revision logs

GREEN = \033[0;32m
CYAN = \033[0;36m
RESET = \033[0m

format:
	@echo "Formatting code..."
	set -e; \
	set -x; \
	ruff check src --fix; \
	ruff format src

lint:
	@echo "Running linters..."
	set -e; \
	set -x; \
	mypy src; \
	ruff check src; \
	ruff format src --check

test:
	@echo "Running tests..."
	pytest src -v -s

test-cov:
	@echo "Running tests with coverage..."
	@echo "Coverage report will be available in the htmlcov directory and in the coverage.xml file"
	pytest src --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml -v -s

up:
	@echo "Starting containers..."
	docker compose up -d --build

down:
	@echo "Stopping containers..."
	docker compose down

down-v:
	@echo "Stopping containers and removing volumes..."
	docker compose down -v

migrate:
	@echo "Applying migrations..."
	docker compose run --rm backend alembic upgrade head

revision:
	@echo "Creating a new migration..."
	docker compose run --rm backend alembic revision --autogenerate -m "$(message)"

message ?= "New migration"

logs:
	@echo "Showing logs..."
	docker compose logs -f

.PHONY: help
help:
	@echo ""
	@echo "${CYAN}Available commands:${RESET}"
	@echo "  ${GREEN}format${RESET}        Format the code"
	@echo "  ${GREEN}lint${RESET}          Run all the linters"
	@echo "  ${GREEN}test${RESET}          Run the tests"
	@echo "  ${GREEN}test-cov${RESET}      Run the tests with coverage"
	@echo "  ${GREEN}up${RESET}            Start the containers and apply migrations"
	@echo "  ${GREEN}down${RESET}          Stop the containers"
	@echo "  ${GREEN}down-v${RESET}        Remove the volumes too"
	@echo "  ${GREEN}migrate${RESET}       Apply migrations"
	@echo "  ${GREEN}revision${RESET}      Create a new migration"
	@echo "  ${GREEN}logs${RESET}          Show logs"
	@echo "  ${GREEN}help${RESET}          Show this message"
