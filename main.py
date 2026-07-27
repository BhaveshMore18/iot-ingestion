from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import SensorReading
from schemas import SensorReadingCreate, SensorReadingOut

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

from tasks import process_reading_async

@app.post("/readings", response_model=SensorReadingOut)
def ingest_reading(reading: SensorReadingCreate, db: Session = Depends(get_db)):
    new_reading = SensorReading(
        sensor_id=reading.sensor_id,
        metric=reading.metric,
        value=reading.value,
    )
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)

    process_reading_async.delay(reading.sensor_id, reading.metric, reading.value)

    return new_reading

from typing import List

@app.get("/readings/{sensor_id}", response_model=List[SensorReadingOut])
def get_readings(sensor_id: str, limit: int = 50, db: Session = Depends(get_db)):
    return (
        db.query(SensorReading)
        .filter(SensorReading.sensor_id == sensor_id)
        .order_by(SensorReading.timestamp.desc())
        .limit(limit)
        .all()
    )

from typing import List

@app.post("/readings/batch", response_model=List[SensorReadingOut])
def ingest_batch(readings: List[SensorReadingCreate], db: Session = Depends(get_db)):
    new_readings = [
        SensorReading(
            sensor_id=r.sensor_id,
            metric=r.metric,
            value=r.value,
        )
        for r in readings
    ]
    db.add_all(new_readings)
    db.commit()
    for r in new_readings:
        db.refresh(r)
    return new_readings