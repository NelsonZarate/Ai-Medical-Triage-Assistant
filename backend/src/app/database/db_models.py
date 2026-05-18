from sqlalchemy import Column, String, Integer, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
import uuid

Base = declarative_base()

class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="patient")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relação com as triagens
    triages = relationship("TriageTable", back_populates="patient")

class TriageTable(Base):
    __tablename__ = "triage_sessions"

    id = Column(String(36), primary_key=True) # UUID gerado no Service
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    patient_name = Column(String(255), nullable=False) # Nome direto para triagens rápidas
    
    # 1. Nurse Data
    initial_symptoms = Column(JSON, nullable=False)
    
    # 2. Safety Agent Data
    is_allowed = Column(Boolean, default=True)
    safety_observations = Column(String(500)) # Mapeia para o 'reason' no Service
    
    # 3. Doctor + RAG + Meds Output
    suggested_diagnosis = Column(String(1000))
    medication_warnings = Column(JSON)
    
    # Estado e Timestamps
    status = Column(String(50), default="IN_PROGRESS")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    patient = relationship("UserTable", back_populates="triages")