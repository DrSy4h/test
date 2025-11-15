"""
GPLink - Data Models
Pydantic schemas for data validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ConsultationStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    COMPLETED = "completed"

class DoctorRole(str, Enum):
    CLINIC = "clinic_doctor"
    CARDIOLOGIST = "cardiologist"
    ADMIN = "admin"

class Doctor(BaseModel):
    name: str
    email: EmailStr
    role: DoctorRole
    hospital_clinic: str
    ic_passport: str  # IC/Passport Number
    mmc_number: str   # MMC Full Registration No.
    nsr_number: Optional[str] = None  # NSR No. (for Cardiologists only)
    password: str  # Hashed password for authentication

class DoctorLogin(BaseModel):
    email: EmailStr
    password: str

class PatientInfo(BaseModel):
    name: str
    age: int
    gender: str
    ic_number: str
    ecg_image: Optional[str] = None  # Filename of ECG image
    xray_image: Optional[str] = None  # Filename of X-Ray image

class ConsultationRequest(BaseModel):
    patient: PatientInfo
    symptoms: str
    vital_signs: dict  # BP, HR, temp, etc.
    clinic_doctor_email: EmailStr
    urgency: str = "normal"  # normal, urgent, emergency

class ConsultationResponse(BaseModel):
    consultation_id: str
    diagnosis: Optional[str] = None
    recommendations: Optional[str] = None
    cardiologist_notes: Optional[str] = None
    cardiologist_email: Optional[EmailStr] = None
    response_date: Optional[datetime] = None

class Consultation(BaseModel):
    consultation_id: str
    patient: PatientInfo
    symptoms: str
    vital_signs: dict
    clinic_doctor_email: EmailStr
    clinic_doctor_name: str
    urgency: str
    status: ConsultationStatus = ConsultationStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Response fields (filled by cardiologist)
    diagnosis: Optional[str] = None
    recommendations: Optional[str] = None
    cardiologist_notes: Optional[str] = None
    cardiologist_email: Optional[EmailStr] = None
    cardiologist_name: Optional[str] = None
    response_date: Optional[datetime] = None
