
docker-bash:
	docker compose exec backend bash

docker-watch:
	docker compose watch

alembic-revision-autogenerate:
	docker compose exec backend alembic revision -m "$(MSG)" --autogenerate

.PHONY: docker-watch docker-bash