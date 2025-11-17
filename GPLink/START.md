# GPLink - Quick Start Guide

## 🚀 How to Run GPLink

### Terminal 1: Start Backend (FastAPI)
```powershell
cd "c:\Users\60163\Downloads\Phyton Tutorial\PYTHON BOOTCAMP\GPLink\backend"
uvicorn main:app --reload
```
✅ Backend will run on: **http://127.0.0.1:8000**  
📖 Swagger docs: **http://127.0.0.1:8000/docs**

### Terminal 2: Start Frontend (Streamlit)
```powershell
cd "c:\Users\60163\Downloads\Phyton Tutorial\PYTHON BOOTCAMP\GPLink"
python -m streamlit run frontend\app.py
```
✅ Frontend will run on: **http://localhost:8501**

---

## 📋 Important Files

### `.env` - MongoDB Configuration
```
MONGODB_ATLAS_CLUSTER_URI=mongodb+srv://drsy4h:uBwLQoc1F00th8dl@cluster0.wqpjziw.mongodb.net/
MONGODB_DATABASE_NAME=gplink_db
```

### `requirements.txt` - Dependencies
- fastapi==0.121.1
- uvicorn==0.38.0
- pymongo==4.15.3
- python-dotenv==1.2.1
- pydantic==2.12.4
- streamlit==1.39.0
- requests==2.32.3
- python-multipart==0.0.20
- email-validator==2.3.0
- bcrypt==4.0.1
- plotly==5.24.1
- reportlab==4.2.5

---

## 🎨 Theme Configuration
- Primary Color: **#9A7D61** (Brown/Tan)
- Copyright: **DRAHMADSYAHID © 2025**

---

## 📁 Project Structure
```
GPLink/
├── backend/
│   ├── main.py          # FastAPI server (15+ endpoints)
│   ├── database.py      # MongoDB connection
│   ├── models.py        # Pydantic schemas (with lab_remarks, image_remarks, provisional_diagnosis)
│   └── crud.py          # CRUD operations (full CRUD)
├── frontend/
│   └── app.py           # Streamlit UI (~2700 lines)
├── uploads/             # Medical images (ECG/X-Ray)
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
└── README.md           # Full documentation
```

---

## ✅ New Features (Nov 2025 - Final Release)
- 📋 **Lab Remarks** - GP adds notes about lab investigations
- 🖼️ **Image Remarks** - GP notes about ECG/X-Ray findings
- 🩺 **Provisional Diagnosis** - GP's initial clinical assessment
- 👨‍⚕️ **Cardiologist Assignment** - Assigned cases visible in statistics
- 🔄 **Follow-up Discussion** - GP sends follow-up questions to cardiologist
- 🗑️ **Auto-Clear Files** - Files clear when entering new consultation page
- 📊 **Smart Display** - Show remarks even without lab/image data

---

## 🔧 Troubleshooting

### If dependencies missing:
```powershell
cd GPLink
pip install -r requirements.txt
```

### If ports are busy:
- Backend uses port 8000
- Frontend uses port 8501 (may auto-change to 8502, 8503, etc.)
- Check task manager if needed

### If MongoDB connection fails:
- Check `.env` file has correct connection string
- Ensure IP is whitelisted in MongoDB Atlas
- Verify internet connection

---

**Made with ❤️ by DRAHMADSYAHID © 2025**
