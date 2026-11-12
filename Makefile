.PHONY: config up down smoke
config:
	docker compose config --quiet
up:
	docker compose up --build
down:
	docker compose down
smoke:
	bash scripts/validate-local.sh
