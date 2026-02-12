ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: up down logs build migrate revision test shell

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose up -d --build

logs:
	docker-compose logs -f bot

migrate:
	docker-compose exec bot poetry run alembic upgrade head

# make revision m="added_something"
revision:
	docker-compose exec bot poetry run alembic revision --autogenerate -m "$(m)"

shell:
	docker-compose exec bot bash

clean:
	docker system prune -a