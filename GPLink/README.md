# GPLink Cardio™ - GP-Cardiologist Consultation Portal

🩺 A consultation platform connecting GP Clinicians with specialist Cardiologists for KPJ Healthcare

## 🌟 Features

### Authentication & Security
- ✅ **Login System** - Secure authentication with bcrypt password hashing
- ✅ **Role-Based Access Control** - Separate access for GP Clinicians, Cardiologists, and Admin
- ✅ **Session Management** - Persistent login sessions with logout functionality
- ✅ **Password Reset** - Admin can reset passwords for any doctor
- ✅ **Registration** - Self-registration for new doctors with email validation

### Core Functionality
- ✅ **Full CRUD Operations** - Create, Read, Update, Delete for consultations and doctors
- ✅ **Real-time Email Validation** - Instant verification for GP and Cardiologist emails
- ✅ **Medical Image Management** - Upload, view, edit, and remove ECG/X-Ray images
- ✅ **PDF Referral Letters** - Auto-generate professional referral letters with optional images
- ✅ **Consultation Workflow** - Pending → Reviewed → Completed status tracking
- ✅ **GP Decision System** - Complete or Continue discussion after cardiologist response
- ✅ **Bulk Operations** - Multi-select delete with confirmation
- ✅ **Doctor Management** - Separate management for Cardiologists and GP Clinicians with inline password reset

### User Interface
- ✅ **KPJ Branded Navigation** - Styled sidebar with KPJ Healthcare logo
- ✅ **Interactive Statistics** - Donut charts and patient file references
- ✅ **Clickable Patient Files** - View detailed consultation records from statistics
- ✅ **Edit Consultations** - Full editing capability for pending consultations
- ✅ **Urgency Indicators** - Color-coded urgency levels (🟢 Normal, 🟡 Urgent, 🔴 Emergency)

### Professional Features
- ✅ **MMC & NSR Validation** - Malaysian Medical Council and National Specialist Register numbers
- ✅ **IC/Passport Number** - Proper identification for all doctors
- ✅ **Role-based Access** - Separate workflows for GP Clinicians and Cardiologists
- ✅ **Comprehensive Vital Signs** - BP, HR, Temp, SpO2, Respiratory Rate tracking

## 📁 Project Structure

```
GPLink/
├── backend/
│   ├── main.py          # FastAPI server (15+ endpoints)
│   ├── database.py      # MongoDB Atlas connection
│   ├── models.py        # Pydantic data models
│   └── crud.py          # Database operations (full CRUD)
├── frontend/
│   └── app.py           # Streamlit interface (~1400+ lines)
├── uploads/             # Medical images storage (ECG/X-Ray)
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies (plotly added)
├── TESTING_GUIDE.md     # Comprehensive testing guide
└── GPLink_Cardio_Testing_Guide.pdf  # Professional PDF testing guide
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```powershell
cd "c:\Users\60163\Downloads\Phyton Tutorial\PYTHON BOOTCAMP\GPLink"
pip install -r requirements.txt
```

**Required packages:**
- fastapi==0.121.1
- uvicorn==0.38.0
- pymongo==4.15.3
- streamlit==1.39.0
- plotly==5.24.1
- reportlab==4.2.5
- requests==2.32.3
- bcrypt==4.0.1 (for password hashing)
- pydantic==2.12.4

### 2. Configure Environment

`.env` file (already configured):

```
MONGODB_ATLAS_CLUSTER_URI=mongodb+srv://drsy4h:uBwLQoc1F00th8dl@cluster0.wqpjziw.mongodb.net/
MONGODB_DATABASE_NAME=gplink_db
```

### 3. Start Backend Server (FastAPI + Swagger)

**Open PowerShell window 1:**
```powershell
cd "c:\Users\60163\Downloads\Phyton Tutorial\PYTHON BOOTCAMP\GPLink\backend"
uvicorn main:app --reload
```

✅ Backend running: `http://127.0.0.1:8000`  
✅ Swagger docs: `http://127.0.0.1:8000/docs`

### 4. Start Frontend (Streamlit)

**Open PowerShell window 2:**
```powershell
cd "c:\Users\60163\Downloads\Phyton Tutorial\PYTHON BOOTCAMP\GPLink\frontend"
streamlit run app.py
```

✅ Frontend: `http://localhost:8501`

## 📖 Usage Guide

### First Time Setup:

1. **Register as Admin** - Create first account with Admin role
   - Fill in: Name, Email, Password (min 6 characters), Hospital/Clinic, IC/Passport, MMC Number
   - Role: Select "Admin"
   - Click "Register" and then "Login"

2. **Login** - Use registered email and password
   - Successful login redirects to Home page
   - Role-based menu appears in sidebar
   - Logout button at bottom of sidebar

### For GP Clinicians:

1. **Register** - Navigate to "👨‍⚕️ Register New Doctor" (or use login page registration)
   - Fill in: Name, Email, Hospital/Clinic, IC/Passport, MMC Number
   - Role: Select "GP Clinician"

2. **Create Consultation** - Go to "➕ New Consultation"
   - Enter your verified email
   - Fill patient details (Name, Age, Gender, IC/Passport No)
   - Add symptoms and vital signs
   - Upload ECG/X-Ray images (optional)
   - Select urgency level

3. **View & Manage** - "📋 View Consultations"
   - Filter by status (All/Pending/Reviewed/Completed)
   - Edit pending consultations (including images)
   - Delete consultations with confirmation
   - Bulk delete multiple consultations

4. **Review Cardiologist Response**
   - When status = "Reviewed", you'll see cardiologist's response
   - **Complete Consultation** - Mark as completed if satisfied
   - **Continue Discussion** - Add follow-up questions (placeholder)

5. **Generate Referral Letter**
   - Choose to include/exclude medical images
   - Download professional PDF referral letter

### For Cardiologists:

1. **Register** - "👨‍⚕️ Register New Doctor"
   - Fill in: Name, Email, Hospital/Clinic, IC/Passport, MMC Number
   - Role: Select "Cardiologist"
   - **NSR Number required** (compulsory for cardiologists)

2. **Respond to Consultations** - "💬 Respond to Consultation"
   - Enter your verified email
   - Select pending consultation from list
   - View patient details, symptoms, vital signs
   - View uploaded ECG/X-Ray images
   - Provide: Diagnosis, Recommendations, Additional Notes
   - Submit response (status → "Reviewed")

### For Admin:

**"👥 Manage Doctors"** - Full administrative features
- **Search** doctors by email
- **Separate sections:**
  - ❤️ Cardiologists (with NSR numbers)
  - 🩺 GP Clinicians
- **3-Column Actions per Doctor:**
  - ✏️ **Edit** - Update doctor information
  - 🔑 **Reset Password** - Set new password (min 6 characters)
  - 🗑️ **Delete** - Remove doctor with confirmation

**"👨‍⚕️ Register New Doctor"** - Create new accounts for staff

**Full System Access** - Admin can:
- View all consultations (not filtered by user)
- Create consultations on behalf of GPs
- Respond as Cardiologist
- Generate reports and statistics
- Manage all doctors

### Statistics & Analytics:

**"📊 Statistics"** - System overview
- Total consultations/doctors metrics
- Interactive donut chart (status distribution)
- Statistics table with percentages
- **Patient File References:**
  - Click 📁 Consultation ID to view full patient file
  - Shows: Patient info, clinical data, vital signs, images, responses
  - Close button to return to list

## 🔌 API Endpoints

### Authentication
- `POST /api/doctors/register` - Register new doctor with password hashing (bcrypt)
- `POST /api/doctors/login` - Login with email/password authentication
- `PUT /api/doctors/{email}/password` - Reset/update doctor password (Admin only)

### Doctors Management
- `GET /api/doctors` - Get all doctors
- `GET /api/doctors/{email}` - Get doctor by email
- `PUT /api/doctors/{email}` - Update doctor information
- `DELETE /api/doctors/{email}` - Delete doctor

### Consultations
- `POST /api/consultations` - Create consultation
- `GET /api/consultations` - Get all consultations (optional status filter)
- `GET /api/consultations/{id}` - Get specific consultation
- `PUT /api/consultations/{id}` - Update consultation details
- `PUT /api/consultations/{id}/respond` - Cardiologist response
- `PUT /api/consultations/{id}/complete` - Mark as completed
- `DELETE /api/consultations/{id}` - Delete consultation

### Medical Images
- `POST /api/consultations/{id}/upload-ecg` - Upload ECG image
- `POST /api/consultations/{id}/upload-xray` - Upload X-Ray image
- `GET /uploads/{filename}` - Serve uploaded images

### System
- `GET /api/stats` - Get system statistics
- `GET /` - Health check

## 🧪 Testing

See **TESTING_GUIDE.md** or **GPLink_Cardio_Testing_Guide.pdf** for:
- 10 comprehensive test cases
- Sample test data
- Expected results
- Bug reporting template

## 💻 Tech Stack

- **Backend:** FastAPI 0.121.1, Python 3.12
- **Database:** MongoDB Atlas (cluster0.wqpjziw.mongodb.net)
- **Frontend:** Streamlit 1.39.0
- **Charts:** Plotly 5.24.1
- **PDF:** ReportLab 4.2.5
- **Validation:** Pydantic 2.12.4
- **Server:** Uvicorn 0.38.0

## 🎨 Branding

- **Theme Color:** #9A7D61 (Brown/Tan)
- **Logo:** KPJ Healthcare
- **Sidebar:** Brown navigation with white text
- **Hover:** Darker brown (#7D6550)
- **Selected:** Dark brown (#6B5640)

## 🔧 Troubleshooting

**Backend not starting:**
- Check MongoDB connection: Already connected to cluster0.wqpjziw.mongodb.net
- Ensure port 8000 is available
- Verify all dependencies installed

**Frontend can't connect:**
- Ensure backend is running on `http://127.0.0.1:8000`
- Check API_URL in frontend/app.py
- Use separate PowerShell windows for stability

**Email validation errors:**
- Doctor must be registered first
- Check email spelling and role
- GP: role = "clinic_doctor", Cardiologist: role = "cardiologist"

**Images not displaying:**
- Check uploads/ directory exists
- Verify file uploaded successfully
- Ensure correct image URL format

**Styling not applying:**
- Hard refresh browser (Ctrl+Shift+R or Ctrl+F5)
- Restart Streamlit server
- Clear browser cache

## 📝 Recent Updates

### Latest Changes (Nov 2025):
- ✅ **Authentication System** - Login/logout with bcrypt password hashing (Python 3.12 compatible)
- ✅ **Role-Based Access** - GP Clinician, Cardiologist, and Admin roles with separate menus
- ✅ **Password Reset** - Admin can reset any doctor's password via inline actions
- ✅ **Forgot Password** - Help text on login page directing users to admin
- ✅ **Session State** - Persistent authentication across page navigation
- ✅ Added KPJ Healthcare logo in sidebar
- ✅ Styled navigation menu with brown theme (#9A7D61)
- ✅ Implemented GP decision system (Complete/Continue)
- ✅ Added doctor management page with 3-column actions (Edit/Reset/Delete)
- ✅ Statistics with donut charts and clickable patient files
- ✅ Real-time email validation for GP and Cardiologist
- ✅ Edit consultation with image upload/remove
- ✅ Bulk delete with confirmation dialogs
- ✅ Changed IC Number to IC/Passport No throughout
- ✅ Urgency selectbox with color indicators
- ✅ Complete consultation with confirmation prompt
- ✅ Login page branding with "DRAHMADSYAHID © 2025" footer

## 🚀 Future Enhancements

- [ ] Follow-up discussion thread between GP and Cardiologist
- [ ] Email notifications for new consultations/responses
- [ ] User authentication & authorization
- [ ] Advanced analytics and reporting
- [ ] Export data to Excel/CSV
- [ ] Audit trail and logging
- [ ] Mobile responsive design
- [ ] Multi-language support

## 👨‍💻 Author

**DRAHMADSYAHID © 2025**  
Repository: DrSy4h/test (main branch)

Made with ❤️ for KPJ Healthcare to improve GP-Cardiologist collaboration
