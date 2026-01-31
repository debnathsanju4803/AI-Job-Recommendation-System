.PHONY: help setup run test clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make setup       - Setup virtual environment and install dependencies"
	@echo "  make run         - Run the API server"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean temporary files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up   - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"

setup:
	@./scripts/setup.sh

run:
	@python run.py

test:
	@python tests/test_complete.py

clean:
	@find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true

docker-build:
	@docker-compose build

docker-up:
	@docker-compose up -d

docker-down:
	@docker-compose down
