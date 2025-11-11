.PHONY: help setup build run stop clean logs cli examples

# Default target
help:
	@echo "🤖 Agentic AI Demo - Available Commands"
	@echo ""
	@echo "Setup & Build:"
	@echo "  make setup          - Initial setup (pull model, build containers)"
	@echo "  make build          - Build Docker containers"
	@echo ""
	@echo "Running:"
	@echo "  make run            - Start all services"
	@echo "  make stop           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo ""
	@echo "Usage:"
	@echo "  make cli            - Interactive CLI mode"
	@echo "  make examples       - Run all example scenarios"
	@echo "  make example-research    - Run research example"
	@echo "  make example-analysis    - Run analysis example"
	@echo "  make example-coding      - Run coding example"
	@echo ""
	@echo "Monitoring:"
	@echo "  make logs           - View all logs"
	@echo "  make logs-orch      - View orchestrator logs"
	@echo "  make logs-ollama    - View Ollama logs"
	@echo "  make status         - Check service health"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Stop and remove containers"
	@echo "  make clean-all      - Complete cleanup (including volumes)"
	@echo ""
	@echo "UI: http://localhost:8080"
	@echo "API: http://localhost:8000/docs"

# Setup - first time installation
setup:
	@echo "🚀 Setting up Agentic AI Demo..."
	@docker compose pull ollama
	@docker compose up -d ollama
	@echo "⏳ Waiting for Ollama to start..."
	@sleep 10
	@echo "📥 Pulling llama3.1 model (this may take a few minutes)..."
	@docker compose exec ollama ollama pull llama3.1
	@echo "🔨 Building application containers..."
	@docker compose build
	@echo "✅ Setup complete! Run 'make run' to start."

# Build containers
build:
	@echo "🔨 Building containers..."
	@docker compose build

# Start all services
run:
	@echo "🚀 Starting Agentic AI Demo..."
	@docker compose up -d
	@echo "⏳ Waiting for services to be ready..."
	@sleep 5
	@make status
	@echo ""
	@echo "✅ System ready!"
	@echo "🌐 UI:  http://localhost:8080"
	@echo "📡 API: http://localhost:8000/docs"

# Stop services
stop:
	@echo "🛑 Stopping services..."
	@docker compose stop

# Restart services
restart: stop run

# Interactive CLI
cli:
	@docker compose exec orchestrator python cli.py

# Run all examples
examples:
	@echo "🎯 Running all example scenarios..."
	@make example-research
	@make example-analysis
	@make example-coding

# Individual examples
example-research:
	@echo "📚 Running research example..."
	@docker compose exec orchestrator python -m examples.research_task

example-analysis:
	@echo "📊 Running analysis example..."
	@docker compose exec orchestrator python -m examples.analysis_task

example-coding:
	@echo "💻 Running coding example..."
	@docker compose exec orchestrator python -m examples.coding_task

# Monitoring
logs:
	@docker compose logs -f

logs-orch:
	@docker compose logs -f orchestrator

logs-ollama:
	@docker compose logs -f ollama

status:
	@echo "📊 Service Status:"
	@docker compose ps

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	@docker compose down
	@echo "✅ Containers stopped and removed"

clean-all:
	@echo "🧹 Complete cleanup (including volumes)..."
	@docker compose down -v
	@rm -rf outputs/*
	@rm -rf sandbox_workspace/*
	@echo "✅ Complete cleanup done"

# Development helpers
shell:
	@docker compose exec orchestrator /bin/bash

test:
	@docker compose exec orchestrator python -m pytest

format:
	@docker compose exec orchestrator python -m black agents/ tools/ memory/ api/

lint:
	@docker compose exec orchestrator python -m pylint agents/ tools/ memory/ api/

