build:
	docker-compose build
run:
	docker-compose up
down:
	docker-compose down
clean: down
	docker system prune -a
dev: build run