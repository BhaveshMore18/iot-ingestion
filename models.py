from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from datetime import datetime, timezone
from database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, nullable=False, index=True)
    metric = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("ix_sensor_timestamp", "sensor_id", "timestamp"),
    )