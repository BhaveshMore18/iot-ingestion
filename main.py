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