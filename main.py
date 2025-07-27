from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fleet Vehicle Telemetry API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vehicles", response_model=schemas.VehicleOut)
def register_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    existing = crud.get_vehicle_by_vin(db, vehicle.vin)
    if existing:
        raise HTTPException(status_code=400, detail="Vehicle already exists")
    return crud.create_vehicle(db, vehicle)

@app.post("/telemetry", response_model=schemas.TelemetryOut)
def post_telemetry(data: schemas.TelemetryCreate, db: Session = Depends(get_db)):
    telemetry = crud.create_telemetry(db, data)
    if not telemetry:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return telemetry

@app.get("/vehicles/{vin}/latest", response_model=schemas.TelemetryOut)
def get_latest(vin: str, db: Session = Depends(get_db)):
    data = crud.get_latest_telemetry(db, vin)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    return crud.get_alerts(db)
