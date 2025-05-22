from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./hospital.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

app = FastAPI()

# === SQLAlchemy Models ===
class DoctorDB(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialty = Column(String)

class PatientDB(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    disease = Column(String)

Base.metadata.create_all(bind=engine)

# === Pydantic Models ===
class Doctor(BaseModel):
    id: int
    name: str
    specialty: str

class Patient(BaseModel):
    id: int
    name: str
    disease: str

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
