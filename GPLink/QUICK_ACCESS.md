# GPLink Cardio™ - Quick Access Guide

## 🚀 Application Links

### 📱 **Frontend (Main Application)**
```
http://localhost:8501
```
- **Purpose**: User interface for doctors
- **Access**: Login with registered credentials
- **Features**: 
  - Create consultations (GP)
  - Respond to consultations (Cardiologist)
  - Manage doctors (Admin)
  - Generate referral letters
  - View statistics

---

### 🔧 **Backend API**
```
http://127.0.0.1:8000
```
- **Purpose**: REST API server
- **Health Check**: http://127.0.0.1:8000/health
- **Status**: Should return `{"status": "healthy"}`

---

### 📚 **API Documentation (Swagger UI)**
```
http://127.0.0.1:8000/docs
```
- **Purpose**: Interactive API documentation
- **Features**:
  - Test all API endpoints directly
  - View request/response schemas
  - See authentication requirements
  - Try out API calls with sample data

**Available Endpoints**:
- `POST /api/doctors/register` - Register new doctor
- `POST /api/doctors/login` - Login authentication
- `PUT /api/doctors/{email}/password` - Reset password (Admin)
- `GET /api/doctors` - Get all doctors
- `POST /api/consultations` - Create consultation
- `GET /api/consultations` - Get all consultations
- `PUT /api/consultations/{consultation_id}` - Update consultation
- `DELETE /api/consultations/{consultation_id}` - Delete consultation
- `POST /api/upload/ecg/{consultation_id}` - Upload ECG image
- `POST /api/upload/xray/{consultation_id}` - Upload X-Ray image

---

### 📖 **Alternative API Docs (ReDoc)**
```
http://127.0.0.1:8000/redoc
```
- **Purpose**: Clean, readable API documentation
- **Features**:
  - Better for reading and understanding API structure
  - Organized by tags
  - Detailed schema definitions

---

## 🗄️ Database Information

### **MongoDB Atlas**
- **Cluster**: cluster0.wqpjziw.mongodb.net
- **Database Name**: `gplink_db`
- **Collections**:
  - `doctors` - Stores doctor credentials and profiles
  - `consultations` - Stores consultation requests and responses

---

## 🔐 Test Accounts

### **Admin Account**
```
Email: admin@gplink.com
Password: admin123
Role: Admin
Features: Full system access
```

### **GP Clinician Account** (Create your own)
```
Email: [your-email]@hospital.com
Password: [min 6 chars]
Role: GP Clinician
Features: Create consultations, view responses
```

### **Cardiologist Account** (Create your own)
```
Email: [your-email]@cardio.com
Password: [min 6 chars]
Role: Cardiologist
Features: Respond to consultations, view cases
```

---

## 🎨 Theme Colors

```
Primary Brown: #9A7D61
Hover Brown: #7D6450
Selected: #6B5640
```

---

## 📋 Quick Navigation Features

### **For GP Clinicians**:
- 🏠 Home
- ➕ New Consultation (with Auto-Clear Files button)
- 📋 View My Consultations (with response count badge)
- 📊 My Statistics

### **For Cardiologists**:
- 🏠 Home
- 💬 Respond to Consultation (with pending count badge)
- 📋 View My Responses (shows assigned + reviewed cases)
- 📊 My Statistics (includes assigned pending consultations)

### **For Admins**:
- 🏠 Home
- 👨‍⚕️ Register New Doctor
- 👥 Manage Doctors (with inline password reset)
- ➕ New Consultation
- 💬 Respond to Consultation
- 📋 View Consultations (all cases)
- 📊 Statistics (global)

---

## 🔔 Notification System

### **GP Clinicians**:
- Badge shows count of consultations with responses
- Example: `📋 View My Consultations (3)` = 3 cases with cardiologist responses

### **Cardiologists**:
- Badge shows count of pending consultations
- Example: `💬 Respond to Consultation (5)` = 5 pending cases awaiting response

---

## 🚦 How to Start

### **1. Start Backend Server**
```powershell
cd "c:\Users\60163\Downloads\Phyton Tutorial\PYTHON BOOTCAMP\GPLink"
.\myvenv\Scripts\Activate.ps1
cd backend
uvicorn main:app --reload
```
✅ Backend running on: http://127.0.0.1:8000

### **2. Start Frontend Application**
```powershell
cd "c:\Users\60163\Downloads\Phyton Tutorial\PYTHON BOOTCAMP\GPLink"
.\myvenv\Scripts\Activate.ps1
cd frontend
streamlit run app.py
```
✅ Frontend running on: http://localhost:8501

### **3. Access Application**
Open browser and go to: http://localhost:8501

---

## 📝 Important Notes

1. **Authentication Required**: All pages require login except the login/registration page
2. **Role-Based Access**: Users only see features relevant to their role
3. **Data Filtering**: GPs and Cardiologists only see their own cases; Admin sees all
4. **Password Reset**: Only Admin can reset passwords via "Manage Doctors" page
5. **Session Persistence**: Login session persists until logout or browser close
6. **Notification Badges**: Real-time counters update based on consultation status

---

## 🆘 Troubleshooting

### **Can't access frontend?**
- Check if Streamlit is running on port 8501
- Try: http://localhost:8501 or http://127.0.0.1:8501

### **API not responding?**
- Check if FastAPI backend is running on port 8000
- Visit health check: http://127.0.0.1:8000/health

### **Login not working?**
- Ensure backend is running
- Check MongoDB connection
- Verify credentials (passwords are case-sensitive)

### **Forgot password?**
- Contact Admin to reset via "Manage Doctors" page
- Admin can reset any user's password

---

**Developer**: DRAHMADSYAHID © 2025  
**GitHub**: https://github.com/DrSy4h/test  
**Version**: 1.0
