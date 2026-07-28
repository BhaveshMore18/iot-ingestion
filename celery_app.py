import os
from celery import Celery

broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
backend_url = os.getenv("CELERY_BACKEND_URL", "redis://127.0.0.1:6380/0")

celery_app = Celery("iot_tasks", broker=broker_url, backend=backend_url)