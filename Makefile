.PHONY: help install update update-dev update-check update-package run test lint format clean version inspector

# Variables  
SERVER_FILE = main.py

# Load .env file if it exists
ifneq (,$(wildcard .env))
    include .env
    export
endif

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {if ($$2 ~ /^🚀|^🛠️|^📦/) printf "\n\033[33m%s\033[0m\n", $$2; else printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

_quick-start: ## 🚀 Quick Start Commands:

install: ## Install dependencies
	uv sync
	@echo "✅ Dependencies installed successfully"

run: ## Run FastMCP server
	DANGEROUSLY_OMIT_AUTH=true FREEPIK_API_KEY=$(FREEPIK_API_KEY) uv run fastmcp run $(SERVER_FILE) 

run-stream: ## Run FastMCP stream server
	DANGEROUSLY_OMIT_AUTH=true uv run fastmcp run $(SERVER_FILE)  --transport streamable-http --port 3000	

dev: ## Run in development mode with auto-reload (usage: make dev API_KEY=your_key)
	@if [ -z "$(API_KEY)" ] && [ -z "$(FREEPIK_API_KEY)" ]; then \
		echo "❌ Error: No API key provided. Use make dev API_KEY=your_key or set FREEPIK_API_KEY env var"; \
		exit 1; \
	fi
	DANGEROUSLY_OMIT_AUTH=true FREEPIK_API_KEY=$${API_KEY:-$(FREEPIK_API_KEY)} uv run fastmcp dev $(SERVER_FILE)

version: ## Check FastMCP version
	uv run fastmcp version

_development: ## 🛠️ Development Commands:

format: ## Format code
	uv run ruff format .
	uv run ruff check --fix .

lint: ## Run linting
	uv run ruff check .
	uv run mypy .

clean: ## Clean temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

_dependency: ## 📦 Dependency Management:

update: ## Update all dependencies to their latest versions
	@echo "🔄 Updating all dependencies..."
	uv lock --upgrade
	uv sync
	@echo "✅ Dependencies updated successfully"

update-dev: ## Update only development dependencies
	@echo "🔄 Updating development dependencies..."
	uv lock --upgrade-package mypy --upgrade-package pre-commit --upgrade-package pytest --upgrade-package ruff
	uv sync
	@echo "✅ Development dependencies updated"

update-check: ## Show which dependencies have available updates
	@echo "📋 Checking available updates..."
	uv pip list --outdated

update-package: ## Update a specific package (usage: make update-package PKG=package_name)
	@if [ -z "$(PKG)" ]; then \
		echo "❌ Error: Specify the package to update with PKG=package_name"; \
		exit 1; \
	fi
	@echo "🔄 Updating $(PKG)..."
	uv lock --upgrade-package $(PKG)
	uv sync
	@echo "✅ $(PKG) updated successfully"
