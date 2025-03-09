.PHONY: all create-env build up fill-db

all: create-env build up

create-env:
	@echo 'POSTGRES_USER=postgres' >> .env
	@echo 'POSTGRES_PASSWORD=postgres' >> .env
	@echo 'POSTGRES_DB=postgres' >> .env
	@echo 'POSTGRES_HOST=db' >> .env
	@echo 'POSTGRES_PORT=5432' >> .env
	@echo 'REDIS_URL=redis://redis:6379' >> .env
	@echo 'Env file created'

build:
	@docker-compose build
	@echo 'Build complete'

up:
	@docker-compose up -d
	@echo 'Up complete'
	@sleep 2

fill-db:
	@docker-compose exec web python -m app.commands.generate_fake_data
	@echo 'DB filled'
