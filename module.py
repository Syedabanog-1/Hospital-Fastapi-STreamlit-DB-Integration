from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# === Database Configuration ===
DATABASE_URL = "sqlite:///./hospital.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

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

# === Pydantic Schemas ===
class Doctor(BaseModel):
    id: int
    name: str
    specialty: str

class Patient(BaseModel):
    id: int
    name: str
    disease: str

# === Create Tables ===
Base.metadata.create_all(bind=engine)
