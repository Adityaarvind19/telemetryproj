from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, index=True)
    make = Column(String)
    model = Column(String)

class Telemetry(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    speed = Column(Float)
    fuel_level = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    engine_status = Column(String)

    vehicle = relationship("Vehicle")
