web: uvicorn main:app --host=0.0.0.0 --port=$PORT
release: python -c "import main; print('FastAPI ready!')"
worker: celery -A main.celery worker --loglevel=info  # Optional
