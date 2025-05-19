run:
	poetry run uvicorn src.main:app --reload

curl:
	curl http://127.0.0.1:8000
