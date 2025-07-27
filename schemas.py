from pydantic import BaseModel
from datetime import datetime

class VehicleCreate(BaseModel):
    vin: str
    make: str
    model: str

class VehicleOut(VehicleCreate):
    id: int

    class Config:
        orm_mode = True

class TelemetryCreate(BaseModel):
    vin: str
    speed: float
    fuel_level: float
    latitude: float
    longitude: float
    engine_status: str

class TelemetryOut(TelemetryCreate):
    timestamp: datetime

    class Config:
        orm_mode = True
