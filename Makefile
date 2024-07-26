# Makefile for notification service

# variables
PYTHON = python3
FLAKE8 = flake8
BLACK = black
ALEMBIC = alembic
DOCKER_COMPOSE = docker compose
CONTAINER = notification-service-personal

# declare phony target to avoid make from referencing actual files
.PHONY: lint format migrate all

# lint code with flake8
lint:
	@echo "--------------------"
	@echo "Linting python code with flake8"
	$(FLAKE8) src
	@echo "Linting complete"

# format code with black
format:
	@echo "--------------------"
	@echo "Formatting python code with black"
	$(BLACK) src -l 79
	@echo "Formatting complete"

# run migrations with a temporal container and remove them when done
migrate:
	@echo "--------------------"
	@echo "Running alembic migrations"
	$(ALEMBIC) upgrade head

# run all targets
all: format lint migrate