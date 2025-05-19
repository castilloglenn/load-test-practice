prod:
	poetry run uvicorn src.main:app --reload

dev:
	poetry run fastapi dev src/main.py

curl:
	curl http://127.0.0.1:8000
