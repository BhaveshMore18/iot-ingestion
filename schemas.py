from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SensorReadingCreate(BaseModel):
    sensor_id: str
    metric: str
    value: float

class SensorReadingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: str
    metric: str
    value: float
    timestamp: datetime