from celery import Celery

celery_app = Celery(
    "iot_tasks",
    broker="amqp://guest:guest@localhost:5672//",
    backend="redis://127.0.0.1:6380/0",
)