build:
	docker-compose build
run:
	docker-compose up
down:
	docker-compose down
clean: down
	docker system prune -a
dev: build run
stress_test:
	wrk -t12 -c400 -d30s http://127.0.0.1:8080