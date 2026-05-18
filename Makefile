.PHONY: setup venv install clean run-dev

# Variáveis
VENV = .venv
PYTHON = $(VENV)/bin/python
UV = $(shell which uv)

check-uv:
	@command -v uv >/dev/null 2>&1 || { echo >&2 "Instala o 'uv' para maior rapidez: https://github.com/astral-sh/uv"; }

setup: check-uv venv install

venv:
	@echo "🚀 Criando ambiente virtual..."
	uv venv $(VENV)
	source .venv/bin/activate

install:
	@echo "📦 Instalando dependências..."
	uv sync

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "✨ Limpeza concluída."


down: 
	docker compose down -v --remove-orphans
up: 
	docker compose up --build api database adminer

it:
	docker compose run -it api bash

current:
	docker exec -it (image name) poetry run alembic -c backend/alembic.ini current

migrate:
	docker exec -it (image name) poetry run alembic -c backend/alembic.ini revision --autogenerate -m "${m}"

migrations:
	docker exec -it (image name) poetry run alembic -c backend/alembic.ini upgrade head

test:
	docker exec -it (image name) poetry run pytest

install:
	poetry install
	
setup: install up migrations create_admin popular test 