
DOCKER_COMPOSE_FILE := docker-compose.yml

.PHONY: up down local

# local: clean
# 	mkdir -p logs
# 	cd logs && chroma run --path ../chroma &
build:
	docker build -t multiinstance-llm .

up: build clean
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d 

down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

clean:
	@if [ -d chroma ]; then \
		rm -rf chroma; \
	fi
	@if [ -d logs ]; then \
		rm -rf logs; \
	fi
	