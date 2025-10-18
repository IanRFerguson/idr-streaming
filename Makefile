# Run formatting checks
ruff:
	@ruff check --fix .
	@ruff format . 


# Start the services with Docker Compose
start:
	@docker compose up --build -d;


# Stop all running services
stop:
	@docker compose down;


# View log stream for all services
logs:
	@docker compose logs -f;

#
run:
	@make start && make logs;

#
driver:
	@python devops/map_driver.py