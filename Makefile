build:
	docker-compose build
run:
	docker-compose up
down:
	docker-compose down
clean: down
	docker system prune -a
	rm *.log
dev: build run
stress_test:
	wrk -t12 -c400 -d30s --latency http://127.0.0.1:8080
load_shedding_test:
	wrk -t12 -c400 -d30s -s ./scripts/load-shedder.lua --latency http://127.0.0.1:8080
