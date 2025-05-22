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

class DoctorUpdate(BaseModel):
    name: str
    specialty: str

class Patient(BaseModel):
    id: int
    name: str
    disease: str

class PatientUpdate(BaseModel):
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
    if db.query(DoctorDB).filter(DoctorDB.id == doctor.id).first():
        raise HTTPException(status_code=400, detail="Doctor already exists.")
    db_doctor = DoctorDB(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    return {"message": "Doctor added"}

@app.get("/doctors/")
def get_doctors(db: Session = Depends(get_db)):
    return db.query(DoctorDB).all()

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(DoctorDB).filter(DoctorDB.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, doctor_update: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = db.query(DoctorDB).filter(DoctorDB.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor.name = doctor_update.name
    doctor.specialty = doctor_update.specialty
    db.commit()
    return {"message": "Doctor updated"}

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(DoctorDB).filter(DoctorDB.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor removed"}

# === Patient Routes ===
@app.post("/patients/")
def add_patient(patient: Patient, db: Session = Depends(get_db)):
    if db.query(PatientDB).filter(PatientDB.id == patient.id).first():
        raise HTTPException(status_code=400, detail="Patient already exists.")
    db_patient = PatientDB(**patient.dict())
    db.add(db_patient)
    db.commit()
    return {"message": "Patient added"}

@app.get("/patients/")
def get_patients(db: Session = Depends(get_db)):
    return db.query(PatientDB).all()

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient.name = patient_update.name
    patient.disease = patient_update.disease
    db.commit()
    return {"message": "Patient updated"}

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return {"message": "Patient removed"}
