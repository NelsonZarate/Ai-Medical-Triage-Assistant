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