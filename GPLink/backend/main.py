"""
GPLink - FastAPI Backend with Swagger
Main API server for GPLink consultation system
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models import (
    Doctor, ConsultationRequest, ConsultationResponse,
    ConsultationStatus, DoctorRole
)
import crud
from typing import List, Optional
from pathlib import Path
import json

app = FastAPI(
    title="GPLink API",
    description="Consultation system connecting clinic doctors with cardiologists",
    version="1.0.0"
)

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for serving images
UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# ============= DOCTORS ENDPOINTS =============

@app.post("/api/doctors/register", tags=["Doctors"])
def register_doctor(doctor: Doctor):
    """Register a new doctor (clinic doctor or cardiologist)"""
    result = crud.create_doctor(doctor)
    if result["success"]:
        return {"message": "Doctor registered successfully", "doctor_id": result["doctor_id"]}
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.get("/api/doctors", tags=["Doctors"])
def get_all_doctors():
    """Get all registered doctors"""
    return crud.get_all_doctors()

@app.get("/api/doctors/{email}", tags=["Doctors"])
def get_doctor(email: str):
    """Get doctor by email"""
    doctor = crud.get_doctor_by_email(email)
    if doctor:
        return doctor
    else:
        raise HTTPException(status_code=404, detail="Doctor not found")

@app.put("/api/doctors/{email}", tags=["Doctors"])
def update_doctor(email: str, doctor: Doctor):
    """Update doctor information"""
    result = crud.update_doctor(email, doctor)
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=404, detail=result["error"])

@app.delete("/api/doctors/{email}", tags=["Doctors"])
def delete_doctor(email: str):
    """Delete a doctor by email"""
    result = crud.delete_doctor(email)
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=404, detail=result["error"])

# ============= CONSULTATIONS ENDPOINTS =============

@app.post("/api/consultations", tags=["Consultations"])
def create_consultation(
    consultation: ConsultationRequest,
    clinic_doctor_email: str
):
    """
    Create new consultation request from clinic doctor
    
    - **patient**: Patient information
    - **symptoms**: Patient symptoms description
    - **vital_signs**: BP, HR, temperature, etc.
    - **urgency**: normal, urgent, or emergency
    """
    consultation_data = consultation.dict()
    result = crud.create_consultation(consultation_data, clinic_doctor_email)
    
    if result["success"]:
        return {
            "message": result["message"],
            "consultation_id": result["consultation_id"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.get("/api/consultations", tags=["Consultations"])
def get_consultations(status: Optional[str] = None):
    """
    Get all consultations, optionally filtered by status
    
    - **status**: pending, reviewed, or completed
    """
    return crud.get_all_consultations(status)

@app.get("/api/consultations/{consultation_id}", tags=["Consultations"])
def get_consultation(consultation_id: str):
    """Get specific consultation by ID"""
    consultation = crud.get_consultation(consultation_id)
    if consultation:
        return consultation
    else:
        raise HTTPException(status_code=404, detail="Consultation not found")

@app.get("/api/consultations/doctor/{email}", tags=["Consultations"])
def get_doctor_consultations(email: str):
    """Get all consultations created by a specific clinic doctor"""
    return crud.get_consultations_by_clinic_doctor(email)

@app.put("/api/consultations/{consultation_id}", tags=["Consultations"])
def update_consultation(consultation_id: str, consultation: ConsultationRequest):
    """Update consultation details"""
    result = crud.update_consultation(consultation_id, consultation.dict())
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=404, detail=result["error"])

@app.delete("/api/consultations/{consultation_id}", tags=["Consultations"])
def delete_consultation(consultation_id: str):
    """Delete a consultation by ID"""
    result = crud.delete_consultation(consultation_id)
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=404, detail=result["error"])

@app.put("/api/consultations/{consultation_id}/respond", tags=["Consultations"])
def respond_to_consultation(
    consultation_id: str,
    response: ConsultationResponse,
    cardiologist_email: str
):
    """
    Cardiologist responds to consultation
    
    - **diagnosis**: Medical diagnosis
    - **recommendations**: Treatment recommendations
    - **cardiologist_notes**: Additional notes
    """
    response_data = {
        "diagnosis": response.diagnosis,
        "recommendations": response.recommendations,
        "cardiologist_notes": response.cardiologist_notes
    }
    
    result = crud.update_consultation_response(
        consultation_id,
        response_data,
        cardiologist_email
    )
    
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.put("/api/consultations/{consultation_id}/complete", tags=["Consultations"])
def complete_consultation(consultation_id: str):
    """Mark consultation as completed"""
    result = crud.mark_consultation_completed(consultation_id)
    
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.delete("/api/consultations/{consultation_id}", tags=["Consultations"])
def delete_consultation(consultation_id: str):
    """Delete a consultation"""
    result = crud.delete_consultation(consultation_id)
    
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=404, detail=result["error"])

# ============= HEALTH CHECK =============

# ============= IMAGE UPLOAD ENDPOINTS =============

@app.post("/api/consultations/{consultation_id}/upload-ecg", tags=["Images"])
async def upload_ecg(consultation_id: str, file: UploadFile = File(...)):
    """Upload ECG image for a consultation"""
    try:
        # Read file content
        content = await file.read()
        
        # Save file
        filename = crud.save_uploaded_file(content, file.filename, consultation_id)
        if not filename:
            raise HTTPException(status_code=500, detail="Failed to save file")
        
        # Update consultation with ECG filename
        consultation = crud.get_consultation(consultation_id)
        if not consultation:
            raise HTTPException(status_code=404, detail="Consultation not found")
        
        crud.consultations_collection.update_one(
            {"consultation_id": consultation_id},
            {"$set": {"patient.ecg_image": filename}}
        )
        
        return {
            "message": "ECG image uploaded successfully",
            "filename": filename,
            "url": f"/uploads/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/consultations/{consultation_id}/upload-xray", tags=["Images"])
async def upload_xray(consultation_id: str, file: UploadFile = File(...)):
    """Upload X-Ray image for a consultation"""
    try:
        # Read file content
        content = await file.read()
        
        # Save file
        filename = crud.save_uploaded_file(content, file.filename, consultation_id)
        if not filename:
            raise HTTPException(status_code=500, detail="Failed to save file")
        
        # Update consultation with X-Ray filename
        consultation = crud.get_consultation(consultation_id)
        if not consultation:
            raise HTTPException(status_code=404, detail="Consultation not found")
        
        crud.consultations_collection.update_one(
            {"consultation_id": consultation_id},
            {"$set": {"patient.xray_image": filename}}
        )
        
        return {
            "message": "X-Ray image uploaded successfully",
            "filename": filename,
            "url": f"/uploads/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/images/{filename}", tags=["Images"])
async def get_image(filename: str):
    """Get uploaded image file"""
    file_path = crud.get_file_path(filename)
    if file_path.exists():
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")

# ============= HEALTH CHECK =============

@app.get("/", tags=["Health"])
def health_check():
    """API health check"""
    return {
        "status": "healthy",
        "service": "GPLink API",
        "version": "1.0.0"
    }

@app.get("/api/stats", tags=["Statistics"])
def get_statistics():
    """Get system statistics"""
    all_consultations = crud.get_all_consultations()
    pending = len([c for c in all_consultations if c["status"] == "pending"])
    reviewed = len([c for c in all_consultations if c["status"] == "reviewed"])
    completed = len([c for c in all_consultations if c["status"] == "completed"])
    
    return {
        "total_consultations": len(all_consultations),
        "pending": pending,
        "reviewed": reviewed,
        "completed": completed,
        "total_doctors": len(crud.get_all_doctors())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
