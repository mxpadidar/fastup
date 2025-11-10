from celery import Celery

from fastup.config import REDIS

redis_url = f"redis://{REDIS['host']}:{REDIS['port']}/{REDIS['db']}"


worker = Celery("fastup", broker=redis_url, backend=redis_url)
