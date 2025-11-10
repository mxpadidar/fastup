uvicorn: uvicorn fastup.entrypoints.app:app --host 0.0.0.0 --port ${PORT:-8000} --reload --log-config=./logging.yaml
celery: celery -q -A fastup.entrypoints.worker worker
