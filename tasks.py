from celery_app import celery_app
import time

@celery_app.task
def process_reading_async(sensor_id: str, metric: str, value: float):
    time.sleep(2)  # simulate work — e.g. anomaly detection, alerting, aggregation
    print(f"Processed reading: {sensor_id} - {metric} = {value}")
    return {"sensor_id": sensor_id, "processed": True}