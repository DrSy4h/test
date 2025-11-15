# GPLink Cardio™ - GP-Cardiologist Consultation Portal

🩺 A consultation platform connecting GP Clinicians with specialist Cardiologists

## Features

- ✅ **CRUD Operations** - Create, Read, Update, Delete consultations
- ✅ **FastAPI Backend** - RESTful API with automatic Swagger documentation
- ✅ **MongoDB Database** - NoSQL database for flexible data storage
- ✅ **Streamlit Frontend** - Interactive web interface
- ✅ **Role-based Access** - Separate flows for GP Clinicians and Cardiologists
- ✅ **Medical Image Upload** - Upload and view ECG and X-Ray images
- ✅ **Referral Letter Generation** - Auto-generate PDF referral letters with edit capability
- ✅ **Professional Registration** - MMC, IC/Passport, NSR number validation

## Project Structure

```
GPLink/
├── backend/
│   ├── main.py          # FastAPI server with Swagger
│   ├── database.py      # MongoDB connection
│   ├── models.py        # Pydantic data models
│   └── crud.py          # Database operations
├── frontend/
│   └── app.py           # Streamlit interface
├── uploads/             # Medical images storage
├── .env                 # Environment variables
└── requirements.txt     # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies

```powershell
cd GPLink
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file with your MongoDB connection string:

```
MONGODB_ATLAS_CLUSTER_URI=your_mongodb_uri
MONGODB_DATABASE_NAME=gplink_db
```

### 3. Start Backend Server (FastAPI + Swagger)

```powershell
cd backend
uvicorn main:app --reload
```

Backend will run on: `http://localhost:8000`
Swagger docs available at: `http://localhost:8000/docs`

### 4. Start Frontend (Streamlit)

Open a new terminal:

```powershell
cd frontend
streamlit run app.py
```

Frontend will open in browser automatically

## Usage

### For Clinic Doctors:

1. Register as a clinic doctor
2. Create consultation requests with patient info
3. View consultation status and cardiologist responses

### For Cardiologists:

1. Register as a cardiologist
2. View pending consultations
3. Provide diagnosis and recommendations

## API Endpoints

### Doctors
- `POST /api/doctors/register` - Register new doctor
- `GET /api/doctors` - Get all doctors
- `GET /api/doctors/{email}` - Get doctor by email

### Consultations
- `POST /api/consultations` - Create consultation
- `GET /api/consultations` - Get all consultations
- `GET /api/consultations/{id}` - Get specific consultation
- `PUT /api/consultations/{id}/respond` - Respond to consultation
- `DELETE /api/consultations/{id}` - Delete consultation

### Statistics
- `GET /api/stats` - Get system statistics

### Medical Images
- `POST /api/consultations/{id}/upload-ecg` - Upload ECG image
- `POST /api/consultations/{id}/upload-xray` - Upload X-Ray image
- `GET /api/images/{filename}` - View uploaded image

## Swagger Documentation

Access interactive API documentation at:
`http://localhost:8000/docs`

Features:
- Try out endpoints directly
- View request/response schemas
- See API examples

## Tech Stack

- **Backend:** FastAPI, Python 3.12
- **Database:** MongoDB Atlas
- **Frontend:** Streamlit
- **Validation:** Pydantic
- **Server:** Uvicorn

## Sample Workflow

1. **Clinic Doctor** creates consultation request for patient with chest pain
2. **Upload** ECG and X-Ray images to consultation
3. System stores in MongoDB with status "pending"
4. **Cardiologist** reviews consultation with medical images in Streamlit
5. Cardiologist provides diagnosis and recommendations via API
6. Status updates to "reviewed"
7. Clinic doctor views cardiologist's response with images

## Troubleshooting

**Backend not starting:**
- Check MongoDB connection string in `.env`
- Ensure port 8000 is available

**Frontend can't connect:**
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `main.py`

**Database errors:**
- Verify MongoDB Atlas IP whitelist
- Check database credentials

## Future Enhancements

- [ ] Authentication & Authorization
- [ ] File upload for medical reports
- [ ] Real-time notifications
- [ ] Email alerts
- [ ] Advanced search and filtering
- [ ] Analytics dashboard

## Author

Made with ❤️ for better healthcare collaboration
