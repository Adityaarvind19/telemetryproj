from sqlalchemy.orm import Session
from models import Vehicle, Telemetry
from schemas import VehicleCreate, TelemetryCreate
from datetime import datetime

def get_vehicle_by_vin(db: Session, vin: str):
    return db.query(Vehicle).filter(Vehicle.vin == vin).first()

def create_vehicle(db: Session, vehicle: VehicleCreate):
    db_vehicle = Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def create_telemetry(db: Session, data: TelemetryCreate):
    vehicle = get_vehicle_by_vin(db, data.vin)
    if not vehicle:
        return None
    db_telemetry = Telemetry(
        vehicle_id=vehicle.id,
        speed=data.speed,
        fuel_level=data.fuel_level,
        latitude=data.latitude,
        longitude=data.longitude,
        engine_status=data.engine_status,
        timestamp=datetime.utcnow()
    )
    db.add(db_telemetry)
    db.commit()
    db.refresh(db_telemetry)
    return db_telemetry

def get_latest_telemetry(db: Session, vin: str):
    vehicle = get_vehicle_by_vin(db, vin)
    if not vehicle:
        return None
    return (
        db.query(Telemetry)
        .filter(Telemetry.vehicle_id == vehicle.id)
        .order_by(Telemetry.timestamp.desc())
        .first()
    )

def get_alerts(db: Session):
    alerts = []
    telemetry = db.query(Telemetry).all()
    for t in telemetry:
        if t.speed > 100:
            alerts.append(f"Vehicle {t.vehicle.vin} overspeeding at {t.speed} km/h")
        if t.fuel_level < 10:
            alerts.append(f"Vehicle {t.vehicle.vin} low fuel: {t.fuel_level}%")
        if t.engine_status != "OK":
            alerts.append(f"Vehicle {t.vehicle.vin} engine issue: {t.engine_status}")
    return alerts
