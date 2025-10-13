isort:
	@isort src --profile black --line-width 120 

start:
	@docker compose up --build -d;

stop:
	@docker compose down;

logs:
	@docker compose logs -f;