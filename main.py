from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

# === Database Setup ===
DATABASE_URL = "sqlite:///./hospital.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# === FastAPI App ===
app = FastAPI()

# === CORS Middleware for Streamlit ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your Streamlit domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Password Hashing ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

# === Pydantic Schemas ===
class Doctor(BaseModel):
    id: int
    name: str
    specialty: str

class DoctorUpdate(BaseModel):
    name: str = None
    specialty: str = None

class Patient(BaseModel):
    id: int
    name: str
    disease: str

class PatientUpdate(BaseModel):
    name: str = None
    disease: str = None

class LoginRequest(BaseModel):
    username: str
    password: str

# === Dependency for DB session ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Auth Route ===
@app.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == request.username).first()
    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

# === Helper: Create Default Admin if Not Exists ===
@app.on_event("startup")
def create_default_admin():
    db = SessionLocal()
    if not db.query(UserDB).filter_by(username="admin").first():
        hashed = pwd_context.hash("password123")
        db.add(UserDB(username="admin", hashed_password=hashed))
        db.commit()
    db.close()

# === Doctor Routes ===
@app.post("/doctors/")
def add_doctor(doctor: Doctor, db: Session = Depends(get_db)):
    if db.query(DoctorDB).filter(DoctorDB.id == doctor.id).first():
        raise HTTPException(status_code=400, detail="Doctor already exists.")
    db.add(DoctorDB(**doctor.dict()))
    db.commit()
    return {"message": "Doctor added"}

@app.get("/doctors/")
def get_doctors(db: Session = Depends(get_db)):
    doctors = db.query(DoctorDB).all()
    return [{"id": d.id, "name": d.name, "specialty": d.specialty} for d in doctors]

@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, doctor_update: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = db.query(DoctorDB).filter(DoctorDB.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if doctor_update.name:
        doctor.name = doctor_update.name
    if doctor_update.specialty:
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
    db.add(PatientDB(**patient.dict()))
    db.commit()
    return {"message": "Patient added"}

@app.get("/patients/")
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(PatientDB).all()
    return [{"id": p.id, "name": p.name, "disease": p.disease} for p in patients]

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if patient_update.name:
        patient.name = patient_update.name
    if patient_update.disease:
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
