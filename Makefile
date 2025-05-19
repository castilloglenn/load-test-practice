prod:
	poetry run uvicorn src.main:app --reload

dev:
	poetry run fastapi dev src/main.py

curl:
	curl http://127.0.0.1:8000

test:
	poetry run locust -f tests/load/test_locustfile.py --host http://127.0.0.1:8000
