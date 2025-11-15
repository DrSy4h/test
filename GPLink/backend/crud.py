"""
GPLink - CRUD Operations
Database operations for consultations and doctors
"""

from database import consultations_collection, doctors_collection
from models import Consultation, Doctor, ConsultationStatus
from datetime import datetime
from bson import ObjectId
import uuid
import os
import shutil
from pathlib import Path

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

def save_uploaded_file(file_content: bytes, filename: str, consultation_id: str) -> str:
    """Save uploaded image file and return the saved filename"""
    try:
        # Create unique filename with consultation ID
        file_extension = Path(filename).suffix
        unique_filename = f"{consultation_id}_{filename}"
        file_path = UPLOADS_DIR / unique_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return unique_filename
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

def get_file_path(filename: str) -> Path:
    """Get full path to uploaded file"""
    return UPLOADS_DIR / filename

# ============= DOCTORS =============

def create_doctor(doctor: Doctor):
    """Register a new doctor"""
    try:
        doctor_dict = doctor.dict()
        result = doctors_collection.insert_one(doctor_dict)
        return {"success": True, "doctor_id": str(result.inserted_id)}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_doctor_by_email(email: str):
    """Get doctor by email"""
    doctor = doctors_collection.find_one({"email": email})
    if doctor:
        doctor["_id"] = str(doctor["_id"])
    return doctor

def get_all_doctors():
    """Get all registered doctors"""
    doctors = list(doctors_collection.find())
    for doc in doctors:
        doc["_id"] = str(doc["_id"])
    return doctors

def update_doctor(email: str, doctor: Doctor):
    """Update doctor information"""
    try:
        doctor_dict = doctor.dict()
        result = doctors_collection.update_one(
            {"email": email},
            {"$set": doctor_dict}
        )
        if result.modified_count > 0:
            return {"success": True, "message": "Doctor updated successfully"}
        else:
            return {"success": False, "error": "Doctor not found or no changes made"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_doctor(email: str):
    """Delete doctor by email"""
    try:
        result = doctors_collection.delete_one({"email": email})
        if result.deleted_count > 0:
            return {"success": True, "message": "Doctor deleted successfully"}
        else:
            return {"success": False, "error": "Doctor not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============= CONSULTATIONS =============

def create_consultation(consultation_data: dict, clinic_doctor_email: str):
    """Create new consultation request from clinic doctor"""
    try:
        # Get clinic doctor info
        clinic_doctor = get_doctor_by_email(clinic_doctor_email)
        if not clinic_doctor:
            return {"success": False, "error": "Clinic doctor not found"}
        
        # Generate unique consultation ID
        consultation_id = f"CON-{uuid.uuid4().hex[:8].upper()}"
        
        consultation = {
            "consultation_id": consultation_id,
            "patient": consultation_data["patient"],
            "symptoms": consultation_data["symptoms"],
            "vital_signs": consultation_data["vital_signs"],
            "clinic_doctor_email": clinic_doctor_email,
            "clinic_doctor_name": clinic_doctor["name"],
            "urgency": consultation_data.get("urgency", "normal"),
            "status": ConsultationStatus.PENDING.value,
            "created_at": datetime.now(),
            "diagnosis": None,
            "recommendations": None,
            "cardiologist_notes": None,
            "cardiologist_email": None,
            "cardiologist_name": None,
            "response_date": None
        }
        
        result = consultations_collection.insert_one(consultation)
        return {
            "success": True,
            "consultation_id": consultation_id,
            "message": "Consultation request created successfully"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_consultation(consultation_id: str):
    """Get specific consultation by ID"""
    consultation = consultations_collection.find_one({"consultation_id": consultation_id})
    if consultation:
        consultation["_id"] = str(consultation["_id"])
    return consultation

def get_all_consultations(status: str = None):
    """Get all consultations, optionally filtered by status"""
    query = {}
    if status:
        query["status"] = status
    
    consultations = list(consultations_collection.find(query).sort("created_at", -1))
    for consult in consultations:
        consult["_id"] = str(consult["_id"])
    return consultations

def get_consultations_by_clinic_doctor(email: str):
    """Get all consultations created by a specific clinic doctor"""
    consultations = list(consultations_collection.find(
        {"clinic_doctor_email": email}
    ).sort("created_at", -1))
    
    for consult in consultations:
        consult["_id"] = str(consult["_id"])
    return consultations

def delete_consultation(consultation_id: str):
    """Delete a consultation by ID"""
    try:
        result = consultations_collection.delete_one({"consultation_id": consultation_id})
        if result.deleted_count > 0:
            return {"success": True, "message": "Consultation deleted successfully"}
        else:
            return {"success": False, "error": "Consultation not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_consultation(consultation_id: str, consultation_data: dict):
    """Update consultation details"""
    try:
        # Build update data dynamically
        update_data = {}
        
        if "patient" in consultation_data:
            update_data["patient"] = consultation_data["patient"]
        if "symptoms" in consultation_data:
            update_data["symptoms"] = consultation_data["symptoms"]
        if "vital_signs" in consultation_data:
            update_data["vital_signs"] = consultation_data["vital_signs"]
        if "urgency" in consultation_data:
            update_data["urgency"] = consultation_data["urgency"]
        
        # Handle image URLs (including removal if set to None)
        if "ecg_image_url" in consultation_data:
            update_data["ecg_image_url"] = consultation_data["ecg_image_url"]
        if "xray_image_url" in consultation_data:
            update_data["xray_image_url"] = consultation_data["xray_image_url"]
        
        # Check if consultation exists
        existing = consultations_collection.find_one({"consultation_id": consultation_id})
        if not existing:
            return {"success": False, "error": "Consultation not found"}
        
        # Perform update if there's data to update
        if update_data:
            result = consultations_collection.update_one(
                {"consultation_id": consultation_id},
                {"$set": update_data}
            )
            return {"success": True, "message": "Consultation updated successfully"}
        else:
            return {"success": True, "message": "No changes to update"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_consultation_response(consultation_id: str, response_data: dict, cardiologist_email: str):
    """Cardiologist adds response to consultation"""
    try:
        # Get cardiologist info
        cardiologist = get_doctor_by_email(cardiologist_email)
        if not cardiologist:
            return {"success": False, "error": "Cardiologist not found"}
        
        update_data = {
            "diagnosis": response_data.get("diagnosis"),
            "recommendations": response_data.get("recommendations"),
            "cardiologist_notes": response_data.get("cardiologist_notes"),
            "cardiologist_email": cardiologist_email,
            "cardiologist_name": cardiologist["name"],
            "response_date": datetime.now(),
            "status": ConsultationStatus.REVIEWED.value
        }
        
        result = consultations_collection.update_one(
            {"consultation_id": consultation_id},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return {"success": True, "message": "Response added successfully"}
        else:
            return {"success": False, "error": "Consultation not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def mark_consultation_completed(consultation_id: str):
    """Mark consultation as completed"""
    try:
        result = consultations_collection.update_one(
            {"consultation_id": consultation_id},
            {"$set": {"status": ConsultationStatus.COMPLETED.value}}
        )
        
        if result.modified_count > 0:
            return {"success": True, "message": "Consultation marked as completed"}
        else:
            return {"success": False, "error": "Consultation not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_consultation(consultation_id: str):
    """Delete a consultation"""
    try:
        result = consultations_collection.delete_one({"consultation_id": consultation_id})
        if result.deleted_count > 0:
            return {"success": True, "message": "Consultation deleted successfully"}
        else:
            return {"success": False, "error": "Consultation not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}
