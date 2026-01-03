# Makefile for PlayWise Music Engine

# Default target
.PHONY: help
help:
	@echo "PlayWise Music Engine - Development Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make dev              Run development environment with docker-compose"
	@echo "  make build            Build docker images"
	@echo "  make up               Start services"
	@echo "  make down             Stop services"
	@echo "  make logs             View logs"
	@echo "  make clean            Remove containers and volumes"
	@echo "  make api-install      Install API dependencies"
	@echo "  make web-install      Install web dependencies"
	@echo "  make test-api         Run API tests"
	@echo "  make test-web         Run web tests (placeholder)"

# Development environment
.PHONY: dev
dev:
	docker-compose up --build

# Build docker images
.PHONY: build
build:
	docker-compose build

# Start services
.PHONY: up
up:
	docker-compose up -d

# Stop services
.PHONY: down
down:
	docker-compose down

# View logs
.PHONY: logs
logs:
	docker-compose logs -f

# Clean up
.PHONY: clean
clean:
	docker-compose down -v --remove-orphans

# Install API dependencies
.PHONY: api-install
api-install:
	cd api && pip install -r requirements.txt

# Install web dependencies
.PHONY: web-install
web-install:
	cd web && npm install

# Run API tests
.PHONY: test-api
test-api:
	cd api && python -m pytest tests/ -v

# Run web tests (placeholder)
.PHONY: test-web
test-web:
	@echo "Web tests not yet implemented"