.PHONY: help install start stop restart logs test clean

help:
	@echo "AI Query Router - Available Commands"
	@echo "===================================="
	@echo "make install    - Install Python dependencies"
	@echo "make start      - Start infrastructure services (Redis, Kafka)"
	@echo "make stop       - Stop all services"
	@echo "make restart    - Restart all services"
	@echo "make logs       - View Docker logs"
	@echo "make test       - Run complete flow test"
	@echo "make clean      - Clean up containers and cache"
	@echo "make run        - Run the application"

install:
	pip install -r requirements.txt

start:
	docker-compose up -d
	@echo "Infrastructure started. Redis and Kafka running."

stop:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

test:
	python test_complete_flow.py

run:
	python main.py

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
