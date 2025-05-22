from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from module import (
    DoctorDB, PatientDB, Doctor, Patient,
    SessionLocal
)

app = FastAPI()

# === Dependency ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Doctor Routes ===
@app.post("/doctors/")
def add_doctor(doctor: Doctor, db: Session = Depends(get_db)):
    existing = db.query(DoctorDB).filter(DoctorDB.id == doctor.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Doctor already exists.")
    db_doctor = DoctorDB(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    return {"message": "Doctor added"}

@app.get("/doctors/")
def get_doctors(db: Session = Depends(get_db)):
    return db.query(DoctorDB).all()

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(DoctorDB).filter(DoctorDB.id == doctor_id).first()
    if doctor:
        db.delete(doctor)
        db.commit()
        return {"message": "Doctor removed"}
    raise HTTPException(status_code=404, detail="Doctor not found")

# === Patient Routes ===
@app.post("/patients/")
def add_patient(patient: Patient, db: Session = Depends(get_db)):
    existing = db.query(PatientDB).filter(PatientDB.id == patient.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient already exists.")
    db_patient = PatientDB(**patient.dict())
    db.add(db_patient)
    db.commit()
    return {"message": "Patient added"}

@app.get("/patients/")
def get_patients(db: Session = Depends(get_db)):
    return db.query(PatientDB).all()

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if patient:
        db.delete(patient)
        db.commit()
        return {"message": "Patient removed"}
    raise HTTPException(status_code=404, detail="Patient not found")
