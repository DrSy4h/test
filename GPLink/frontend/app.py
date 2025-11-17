"""
GPLink - Streamlit Frontend
User interface for clinic doctors and cardiologists
"""

import streamlit as st
import requests
import json
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

# API Base URL
API_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="GPLink Cardio™ | GP-Cardiologist Consultation Portal",
    page_icon="🩺",
    layout="wide"
)

# Custom CSS with #9A7D61 color theme
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #9A7D61 0%, #B89A7D 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(154, 125, 97, 0.3);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: #F5F5F5;
        margin: 0.5rem 0 0 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F5EDE4;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #9A7D61;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #9A7D61;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #7D6450;
        box-shadow: 0 4px 8px rgba(154, 125, 97, 0.4);
        transform: translateY(-2px);
    }
    
    /* Sidebar primary button override - use brown theme with guaranteed white text */
    div[data-testid="stSidebar"] .stButton>button {
        background-color: #9A7D61 !important;
        color: white !important;
    }
    div[data-testid="stSidebar"] .stButton>button:hover {
        background-color: #7D6450 !important;
        color: white !important;
    }
    
    /* Success/Info boxes */
    .element-container div[data-testid="stMarkdownContainer"] div[data-testid="stMarkdown"] {
        border-left: 4px solid #9A7D61;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #9A7D61;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #F5EDE4;
        border-left: 4px solid #9A7D61;
        border-radius: 5px;
    }
    
    /* Form submit button specific */
    .stFormSubmitButton>button {
        background-color: #9A7D61;
        color: white;
        width: 100%;
        border-radius: 5px;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .stFormSubmitButton>button:hover {
        background-color: #7D6450;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #9A7D61;
    }
</style>
""", unsafe_allow_html=True)

# ============= HELPER FUNCTIONS =============

def format_datetime(dt_string):
    """Format datetime string to readable format"""
    if not dt_string or dt_string == 'N/A':
        return 'N/A'
    try:
        # Parse ISO format datetime
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        # Format to: 16 Nov 2025, 12:12 PM
        return dt.strftime('%d %b %Y, %I:%M %p')
    except:
        return dt_string

def register_doctor(name, email, role, hospital_clinic, ic_passport, mmc_number, nsr_number=None):
    """Register a new doctor"""
    payload = {
        "name": name,
        "email": email,
        "role": role,
        "hospital_clinic": hospital_clinic,
        "ic_passport": ic_passport,
        "mmc_number": mmc_number
    }
    if nsr_number:
        payload["nsr_number"] = nsr_number
    response = requests.post(f"{API_URL}/doctors/register", json=payload)
    return response.json()

def get_all_doctors():
    """Get all registered doctors"""
    response = requests.get(f"{API_URL}/doctors")
    return response.json()

def update_doctor(old_email, name, email, role, hospital_clinic, ic_passport, mmc_number, nsr_number=None):
    """Update doctor information"""
    payload = {
        "name": name,
        "email": email,
        "role": role,
        "hospital_clinic": hospital_clinic,
        "ic_passport": ic_passport,
        "mmc_number": mmc_number
    }
    if nsr_number:
        payload["nsr_number"] = nsr_number
    response = requests.put(f"{API_URL}/doctors/{old_email}", json=payload)
    return response.json()

def delete_doctor(email):
    """Delete doctor"""
    response = requests.delete(f"{API_URL}/doctors/{email}")
    return response.json()

def create_consultation(patient_data, symptoms, vital_signs, clinic_doctor_email, urgency, 
                        assigned_cardiologist_email=None, lab_investigations=None, 
                        lab_remarks=None, image_remarks=None, provisional_diagnosis=None):
    """Create new consultation"""
    payload = {
        "patient": patient_data,
        "symptoms": symptoms,
        "vital_signs": vital_signs,
        "clinic_doctor_email": clinic_doctor_email,
        "urgency": urgency,
        "assigned_cardiologist_email": assigned_cardiologist_email,
        "lab_investigations": lab_investigations or [],
        "lab_remarks": lab_remarks,
        "image_remarks": image_remarks,
        "provisional_diagnosis": provisional_diagnosis
    }
    response = requests.post(
        f"{API_URL}/consultations?clinic_doctor_email={clinic_doctor_email}",
        json=payload
    )
    return response.json()

def get_consultations(status=None):
    """Get all consultations"""
    url = f"{API_URL}/consultations"
    if status:
        url += f"?status={status}"
    response = requests.get(url)
    return response.json()

def respond_to_consultation(consultation_id, diagnosis, recommendations, notes, cardiologist_email):
    """Cardiologist responds to consultation"""
    payload = {
        "consultation_id": consultation_id,
        "diagnosis": diagnosis,
        "recommendations": recommendations,
        "cardiologist_notes": notes
    }
    response = requests.put(
        f"{API_URL}/consultations/{consultation_id}/respond?cardiologist_email={cardiologist_email}",
        json=payload
    )
    return response.json()

def get_stats():
    """Get system statistics"""
    response = requests.get(f"{API_URL}/stats")
    return response.json()

def upload_ecg(consultation_id, file):
    """Upload ECG image"""
    files = {"file": (file.name, file.getvalue(), file.type)}
    response = requests.post(f"{API_URL}/consultations/{consultation_id}/upload-ecg", files=files)
    return response.json()

def upload_xray(consultation_id, file):
    """Upload X-Ray image"""
    files = {"file": (file.name, file.getvalue(), file.type)}
    response = requests.post(f"{API_URL}/consultations/{consultation_id}/upload-xray", files=files)
    return response.json()

def generate_referral_letter_pdf(consultation, gp_doctor, referral_reason="", include_images=False):
    """Generate referral letter PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#9A7D61'), spaceAfter=30)
    header_style = ParagraphStyle('CustomHeader', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#9A7D61'), spaceAfter=12)
    normal_style = styles['Normal']
    
    # Header
    elements.append(Paragraph("<b>REFERRAL LETTER TO CARDIOLOGIST</b>", title_style))
    elements.append(Paragraph(f"<b>GPLink Cardio™</b><br/>Date: {datetime.now().strftime('%d %B %Y')}", normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # GP Information
    elements.append(Paragraph("<b>From:</b>", header_style))
    elements.append(Paragraph(f"{gp_doctor['name']}<br/>{gp_doctor['hospital_clinic']}<br/>MMC: {gp_doctor.get('mmc_number', 'N/A')}<br/>Email: {gp_doctor['email']}", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Patient Information
    elements.append(Paragraph("<b>Patient Information:</b>", header_style))
    patient = consultation['patient']
    patient_data = [
        ['Name:', patient['name']],
        ['IC/Passport No:', patient['ic_number']],
        ['Age:', f"{patient['age']} years"],
        ['Gender:', patient['gender']]
    ]
    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#9A7D61')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Clinical Information
    elements.append(Paragraph("<b>Presenting Symptoms:</b>", header_style))
    elements.append(Paragraph(consultation['symptoms'], normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Vital Signs
    elements.append(Paragraph("<b>Vital Signs:</b>", header_style))
    vs = consultation['vital_signs']
    vital_data = [
        ['Blood Pressure:', vs.get('blood_pressure', 'N/A')],
        ['Heart Rate:', f"{vs.get('heart_rate', 'N/A')} bpm"],
        ['Temperature:', f"{vs.get('temperature', 'N/A')}°C"],
        ['SpO2:', f"{vs.get('spo2', 'N/A')}%"],
        ['Respiratory Rate:', f"{vs.get('respiratory_rate', 'N/A')} /min"]
    ]
    vital_table = Table(vital_data, colWidths=[2*inch, 2*inch])
    vital_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#9A7D61')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(vital_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Lab Investigations
    if consultation.get('lab_investigations') and len(consultation['lab_investigations']) > 0:
        elements.append(Paragraph("<b>Lab Investigations:</b>", header_style))
        sorted_labs = sorted(consultation['lab_investigations'], key=lambda x: x['date_time'], reverse=True)
        lab_data = [['Test Name', 'Date & Time', 'Result']]
        for lab in sorted_labs:
            lab_data.append([lab['test_name'], lab['date_time'], lab['result']])
        
        lab_table = Table(lab_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        lab_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9A7D61')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
        ]))
        elements.append(lab_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Lab Remarks
        if consultation.get('lab_remarks'):
            elements.append(Paragraph(f"<b>GP's Remarks on Lab Results:</b>", ParagraphStyle('small_header', parent=header_style, fontSize=10)))
            elements.append(Paragraph(consultation['lab_remarks'], normal_style))
        
        elements.append(Spacer(1, 0.2*inch))
    
    # GP's Provisional Diagnosis
    if consultation.get('provisional_diagnosis'):
        elements.append(Paragraph("<b>GP's Provisional Diagnosis:</b>", header_style))
        elements.append(Paragraph(consultation['provisional_diagnosis'], normal_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Medical Images with GP's Remarks
    if include_images:
        patient = consultation['patient']
        if patient.get('ecg_image') or patient.get('xray_image'):
            elements.append(Paragraph("<b>Attached Medical Images:</b>", header_style))
            if patient.get('ecg_image'):
                elements.append(Paragraph(f"• ECG Image: {patient['ecg_image']}", normal_style))
            if patient.get('xray_image'):
                elements.append(Paragraph(f"• X-Ray Image: {patient['xray_image']}", normal_style))
            elements.append(Paragraph("<i>(Images available in digital consultation record)</i>", ParagraphStyle('small', parent=normal_style, fontSize=8, textColor=colors.grey)))
            
            # Image Remarks
            if consultation.get('image_remarks'):
                elements.append(Spacer(1, 0.1*inch))
                elements.append(Paragraph(f"<b>GP's Remarks on Images:</b>", ParagraphStyle('small_header', parent=header_style, fontSize=10)))
                elements.append(Paragraph(consultation['image_remarks'], normal_style))
            
            elements.append(Spacer(1, 0.2*inch))
    
    # Reason for Referral
    if referral_reason:
        elements.append(Paragraph("<b>Reason for Referral:</b>", header_style))
        elements.append(Paragraph(referral_reason, normal_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Urgency
    elements.append(Paragraph(f"<b>Urgency Level:</b> {consultation['urgency'].upper()}", header_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    elements.append(Paragraph("<i>I would appreciate your expert opinion on this patient's cardiac condition. Thank you for your assistance.</i>", normal_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"<b>Yours sincerely,</b><br/>{gp_doctor['name']}<br/>{gp_doctor['hospital_clinic']}", normal_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("<i>Generated by GPLink Cardio™ © 2025 DRAHMADSYAHID</i>", ParagraphStyle('Footer', parent=normal_style, fontSize=8, textColor=colors.grey)))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ============= MAIN APP =============

# Initialize session state for authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

# ============= LOGIN PAGE =============

if not st.session_state.logged_in:
    # Custom header
    st.markdown("""
    <div class="main-header">
        <h1>GPLink Cardio™</h1>
        <p>GP-Cardiologist Consultation Portal | Connecting GP Clinicians with Cardiologists for Better Patient Care</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar logo
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <img src="https://bmcc.org.my/cms/images/files/2024/08/KPJ-Logo-1024x213.png" 
             alt="KPJ Healthcare Logo" 
             style="max-width: 250px; width: 100%; height: auto;">
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    st.markdown("### 🔐 Login")
    st.markdown("Please login to access GPLink Cardio™")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Sign In")
        login_email = st.text_input("Email", key="login_email", placeholder="your.email@hospital.com")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("🔓 Login", type="primary", use_container_width=True):
            if login_email and login_password:
                try:
                    response = requests.post(
                        f"{API_URL}/doctors/login",
                        json={"email": login_email, "password": login_password}
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.logged_in = True
                        st.session_state.user = result["user"]
                        st.success(f"✅ Welcome back, {result['user']['name']}!")
                        st.rerun()
                    else:
                        error_msg = response.json().get("detail", "Login failed")
                        st.error(f"❌ {error_msg}")
                except Exception as e:
                    st.error(f"❌ Error connecting to server: {e}")
            else:
                st.warning("⚠️ Please enter both email and password")
        
        # Forgot password help
        st.info("🔑 **Forgot Password?** Contact your Admin to reset your password.")
    
    with col2:
        st.markdown("#### New User?")
        st.info("""
        **First time here?**
        
        Register as a doctor to access GPLink Cardio™:
        
        - **GP Clinicians**: Create consultations, get expert advice
        - **Cardiologists**: Review cases, provide recommendations
        
        Click below to register!
        """)
        
        if st.button("👨‍⚕️ Register New Account", use_container_width=True):
            st.session_state.show_registration = True
            st.rerun()
    
    # Show registration form if button clicked
    if 'show_registration' in st.session_state and st.session_state.show_registration:
        st.markdown("---")
        st.markdown("### 👨‍⚕️ Register New Doctor")
        
        name = st.text_input("Full Name *", help="Full name as per registration")
        email = st.text_input("Email *", help="Professional email address", key="reg_email")
        password = st.text_input("Password *", type="password", help="Create a secure password (min 6 characters)", key="reg_password")
        confirm_password = st.text_input("Confirm Password *", type="password", help="Re-enter your password")
        role = st.selectbox("Role *", ["GP Clinician", "Cardiologist", "Admin"], help="Select your role")
        hospital_clinic = st.text_input("Hospital/Clinic Name *", help="Current workplace")
        ic_passport = st.text_input("IC/Passport Number *", help="National ID or Passport number")
        mmc_number = st.text_input("MMC Full Registration No. *", help="Malaysian Medical Council registration number")
        
        # NSR number - compulsory for cardiologists
        nsr_number = ""
        if role == "Cardiologist":
            nsr_number = st.text_input("NSR No. * (Compulsory for Cardiologists)", help="National Specialist Register number")
        
        col_reg1, col_reg2 = st.columns(2)
        with col_reg1:
            if st.button("✅ Register", type="primary", use_container_width=True):
                # Validation
                if password != confirm_password:
                    st.error("❌ Passwords do not match!")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters long!")
                else:
                    if role == "Cardiologist":
                        all_filled = name and email and password and hospital_clinic and ic_passport and mmc_number and nsr_number
                        if not nsr_number:
                            st.error("❌ NSR No. is compulsory for Cardiologists!")
                    else:
                        all_filled = name and email and password and hospital_clinic and ic_passport and mmc_number
                    
                    if all_filled:
                        try:
                            if role == "GP Clinician":
                                role_backend = "clinic_doctor"
                            elif role == "Cardiologist":
                                role_backend = "cardiologist"
                            else:
                                role_backend = "admin"
                            doctor_data = {
                                "name": name,
                                "email": email,
                                "password": password,
                                "role": role_backend,
                                "hospital_clinic": hospital_clinic,
                                "ic_passport": ic_passport,
                                "mmc_number": mmc_number,
                                "nsr_number": nsr_number if role == "Cardiologist" else None
                            }
                            
                            response = requests.post(f"{API_URL}/doctors/register", json=doctor_data)
                            if response.status_code == 200:
                                st.success("✅ Registration successful! Please login with your credentials.")
                                del st.session_state.show_registration
                                st.rerun()
                            elif response.status_code == 409:
                                # Duplicate email - set password
                                st.warning(f"⚠️ Email {email} already exists!")
                                st.info("💡 Setting password...")
                                
                                password_response = requests.put(
                                    f"{API_URL}/doctors/{email}/password",
                                    json={"password": password}
                                )
                                
                                if password_response.status_code == 200:
                                    st.success(f"✅ Password set! You can now login.")
                                    del st.session_state.show_registration
                                    st.rerun()
                                else:
                                    st.error(f"❌ Failed to set password")
                            else:
                                error_detail = response.json().get('detail', 'Registration failed')
                                st.error(f"❌ {error_detail}")
                        except requests.exceptions.RequestException as req_err:
                            st.error(f"❌ Connection Error: {req_err}")
                            st.info("💡 Make sure backend is running on http://localhost:8000")
                        except Exception as e:
                            st.error(f"❌ Error: {type(e).__name__}: {str(e)}")
                    else:
                        st.warning("⚠️ Please fill in all required fields (marked with *)")
        
        with col_reg2:
            if st.button("← Back to Login", use_container_width=True):
                del st.session_state.show_registration
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0; color: #9A7D61;">
        <p style="font-size: 1rem; font-weight: 600; margin: 0;">DRAHMADSYAHID © 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# ============= LOGGED IN - MAIN APP =============

# Custom header with theme color
st.markdown("""
<div class="main-header">
    <h1>GPLink Cardio™</h1>
    <p>GP-Cardiologist Consultation Portal | Connecting GP Clinicians with Cardiologists for Better Patient Care</p>
</div>
""", unsafe_allow_html=True)

# Sidebar logo and navigation
# Sidebar logo and navigation
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <img src="https://bmcc.org.my/cms/images/files/2024/08/KPJ-Logo-1024x213.png" 
         alt="KPJ Healthcare Logo" 
         style="max-width: 250px; width: 100%; height: auto;">
</div>
""", unsafe_allow_html=True)

# User info in sidebar
st.sidebar.markdown(f"### 👤 {st.session_state.user['name']}")
if st.session_state.user['role'] == 'clinic_doctor':
    role_display = "GP Clinician"
elif st.session_state.user['role'] == 'cardiologist':
    role_display = "Cardiologist"
else:
    role_display = "Admin"
st.sidebar.markdown(f"**Role:** {role_display}")
st.sidebar.markdown(f"**Hospital:** {st.session_state.user['hospital_clinic']}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Navigation Menu")

# Role-based navigation with notification counters
user_role = st.session_state.user['role']
user_email = st.session_state.user['email']

# Get notification counts
try:
    all_consultations = get_consultations(None)  # Get all consultations
    
    if user_role == 'clinic_doctor':
        # Count reviewed/completed consultations for this GP
        my_consultations = [c for c in all_consultations if c['clinic_doctor_email'] == user_email]
        new_responses = len([c for c in my_consultations if c['status'] in ['reviewed', 'completed']])
        responses_badge = f" ({new_responses})" if new_responses > 0 else ""
    elif user_role == 'cardiologist':
        # Count pending consultations: assigned to me (priority) + unassigned (available)
        assigned_to_me = [c for c in all_consultations if c['status'] == 'pending' and c.get('assigned_cardiologist_email') == user_email]
        unassigned = [c for c in all_consultations if c['status'] == 'pending' and not c.get('assigned_cardiologist_email')]
        
        assigned_count = len(assigned_to_me)
        unassigned_count = len(unassigned)
        
        if assigned_count > 0 and unassigned_count > 0:
            pending_badge = f" (🔴{assigned_count} + {unassigned_count})"  # Red badge for assigned + unassigned count
        elif assigned_count > 0:
            pending_badge = f" (🔴{assigned_count})"  # Only assigned cases (priority)
        elif unassigned_count > 0:
            pending_badge = f" ({unassigned_count})"  # Only unassigned cases
        else:
            pending_badge = ""
except:
    responses_badge = ""
    pending_badge = ""

if user_role == 'clinic_doctor':
    # GP Clinician menu
    navigation_options = [
        "🏠 Home",
        "➕ New Consultation",
        f"📋 View My Consultations{responses_badge}",
        "📊 My Statistics"
    ]
elif user_role == 'cardiologist':
    # Cardiologist menu
    navigation_options = [
        "🏠 Home",
        f"💬 Respond to Consultation{pending_badge}",
        "📋 View My Responses",
        "📊 My Statistics"
    ]
elif user_role == 'admin':
    # Admin menu - full access
    navigation_options = [
        "🏠 Home",
        "👨‍⚕️ Register New Doctor",
        "👥 Manage Doctors",
        "➕ New Consultation",
        "💬 Respond to Consultation",
        "📋 View Consultations",
        "📊 Statistics"
    ]
else:
    # Fallback menu
    navigation_options = ["🏠 Home"]

# Navigation with radio buttons
page = st.sidebar.radio(
    "",
    navigation_options,
    label_visibility="collapsed"
)

# Normalize page name (remove notification badges)
import re
page_clean = re.sub(r'\s*\(\d+\)$', '', page)  # Remove (number) at end

# Custom CSS for navigation styling
st.sidebar.markdown("""
<style>
div[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: #9A7D61 !important;
    color: white !important;
    padding: 0.75rem 1rem !important;
    border-radius: 0.5rem !important;
    margin-bottom: 0.5rem !important;
    display: block !important;
    cursor: pointer !important;
    font-weight: 500 !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: #7D6550 !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
    background-color: #6B5640 !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Logout button with HTML
logout_clicked = st.sidebar.button("LOGOUT", use_container_width=True, key="logout_btn")
st.sidebar.markdown("""
<style>
button[kind="secondary"] {
    background-color: #9A7D61 !important;
    color: white !important;
    border: none !important;
    font-weight: bold !important;
}
button[kind="secondary"]:hover {
    background-color: #7D6450 !important;
}
button[kind="secondary"] p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

if logout_clicked:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# ============= HOME PAGE =============

if page_clean == "🏠 Home":
    st.header("Welcome to GPLink!")
    st.markdown("""
    ### About GPLink Cardio™
    GPLink Cardio™ is a consultation system that connects GP clinicians with specialist cardiologists.
    
    **For GP Clinicians:**
    - Submit consultation requests for patients with cardiac concerns
    - Get expert advice from cardiologists
    - Generate referral letters
    - Track consultation status
    
    **For Cardiologists:**
    - Review consultation requests from GP clinicians
    - Provide diagnosis and recommendations
    - Help improve patient outcomes
    
    **Getting Started:**
    1. Register as a doctor (GP Clinician or Cardiologist)
    2. GP Clinicians can create new consultations and generate referral letters
    3. Cardiologists can review and respond to consultations
    """)
    
    try:
        stats = get_stats()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Consultations", stats["total_consultations"])
        col2.metric("Pending", stats["pending"], delta="🔴")
        col3.metric("Reviewed", stats["reviewed"], delta="🟡")
        col4.metric("Completed", stats["completed"], delta="🟢")
    except:
        st.warning("⚠️ Please start the backend server first: `cd backend && uvicorn main:app --reload`")
    
    # API Documentation Link
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <p style="font-size: 0.9rem;">
            📚 <b>API Documentation (Swagger):</b> 
            <a href="http://127.0.0.1:8000/docs" target="_blank" style="color: #9A7D61; text-decoration: none; font-weight: 600;">
                http://127.0.0.1:8000/docs
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer on home page
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0; color: #9A7D61;">
        <p style="font-size: 1rem; font-weight: 600; margin: 0;">DRAHMADSYAHID © 2025</p>
    </div>
    """, unsafe_allow_html=True)

# ============= REGISTER DOCTOR =============

elif page_clean == "👨‍⚕️ Register New Doctor":
    st.header("Register New Doctor")
    
    name = st.text_input("Full Name *", key="reg_name", help="Full name as per registration")
    email = st.text_input("Email *", key="reg_email", help="Professional email address")
    password = st.text_input("Password *", key="reg_password", type="password", help="Create a secure password")
    confirm_password = st.text_input("Confirm Password *", key="reg_confirm_password", type="password", help="Re-enter your password")
    role = st.selectbox("Role *", ["GP Clinician", "Cardiologist", "Admin"], key="reg_role", help="Select your role")
    hospital_clinic = st.text_input("Hospital/Clinic Name *", key="reg_hospital", help="Current workplace")
    ic_passport = st.text_input("IC/Passport Number *", key="reg_ic", help="National ID or Passport number")
    mmc_number = st.text_input("MMC Full Registration No. *", key="reg_mmc", help="Malaysian Medical Council registration number")
    
    # NSR number - compulsory for cardiologists, appears dynamically
    nsr_number = ""
    if role == "Cardiologist":
        nsr_number = st.text_input("NSR No. * (Compulsory for Cardiologists)", key="reg_nsr", help="National Specialist Register number - Required for Cardiologists")
    
    if st.button("Register", type="primary"):
        # Validate passwords match
        if password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif len(password) < 6:
            st.error("❌ Password must be at least 6 characters long!")
        else:
            # Validate all required fields with better checking
            missing_fields = []
            if not name.strip(): missing_fields.append("Full Name")
            if not email.strip(): missing_fields.append("Email")
            if not password: missing_fields.append("Password")
            if not hospital_clinic.strip(): missing_fields.append("Hospital/Clinic Name")
            if not ic_passport.strip(): missing_fields.append("IC/Passport Number")
            if not mmc_number.strip(): missing_fields.append("MMC Full Registration No.")
            
            # NSR required for Cardiologist
            if role == "Cardiologist" and not nsr_number.strip():
                missing_fields.append("NSR No.")
            
            if missing_fields:
                st.warning(f"⚠️ Please fill in: {', '.join(missing_fields)}")
            else:
                # Convert role display to backend format
                if role == "GP Clinician":
                    role_backend = "clinic_doctor"
                elif role == "Cardiologist":
                    role_backend = "cardiologist"
                else:
                    role_backend = "admin"
                
                # Prepare doctor data
                doctor_data = {
                    "name": name,
                    "email": email,
                    "password": password,
                    "role": role_backend,
                    "hospital_clinic": hospital_clinic,
                    "ic_passport": ic_passport,
                    "mmc_number": mmc_number,
                    "nsr_number": nsr_number if role == "Cardiologist" else None
                }
                
                try:
                    response = requests.post(f"{API_URL}/doctors/register", json=doctor_data)
                    
                    if response.status_code == 200:
                        st.success(f"✅ Doctor registered successfully!")
                        st.rerun()  # Refresh to clear form
                    elif response.status_code == 409:
                        # Duplicate email - set password instead
                        st.warning(f"⚠️ Email {email} already exists in database!")
                        st.info("💡 Setting password for existing user...")
                        
                        password_response = requests.put(
                            f"{API_URL}/doctors/{email}/password",
                            json={"password": password}
                        )
                        
                        if password_response.status_code == 200:
                            st.success(f"✅ Password set successfully for {email}! You can now login.")
                        else:
                            st.error(f"❌ Failed to set password: {password_response.json().get('detail', 'Unknown error')}")
                    else:
                        error_detail = response.json().get('detail', 'Registration failed')
                        st.error(f"❌ Unexpected error (Status {response.status_code}): {error_detail}")
                except Exception as e:
                    st.error(f"❌ Exception: {type(e).__name__}: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())

# ============= MANAGE DOCTORS =============

elif page_clean == "👥 Manage Doctors":
    st.header("Manage Doctors")
    
    try:
        # Get all doctors
        doctors = get_all_doctors()
        
        if doctors:
            # Separate doctors by role
            cardiologists = [d for d in doctors if d['role'] == 'cardiologist']
            gp_clinicians = [d for d in doctors if d['role'] == 'clinic_doctor']
            
            st.write(f"**Total Doctors:** {len(doctors)} (Cardiologists: {len(cardiologists)}, GP Clinicians: {len(gp_clinicians)})")
            
            # Search filter
            search_email = st.text_input("🔍 Search by email", placeholder="Enter email to search...")
            
            # CARDIOLOGISTS SECTION
            st.markdown("---")
            st.subheader("❤️ Cardiologists")
            
            if search_email:
                filtered_cardiologists = [d for d in cardiologists if search_email.lower() in d['email'].lower()]
            else:
                filtered_cardiologists = cardiologists
            
            if filtered_cardiologists:
                for doctor in filtered_cardiologists:
                    with st.expander(f"❤️ {doctor['name']} ({doctor['email']})"):
                        # Display current info
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Name:** {doctor['name']}")
                            st.write(f"**Email:** {doctor['email']}")
                            st.write(f"**Hospital/Clinic:** {doctor['hospital_clinic']}")
                        
                        with col2:
                            st.write(f"**IC/Passport:** {doctor['ic_passport']}")
                            st.write(f"**MMC No:** {doctor.get('mmc_number', 'N/A')}")
                            st.write(f"**NSR No:** {doctor.get('nsr_number', 'N/A')}")
                        
                        st.markdown("---")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns([1, 1, 1])
                        
                        with col1:
                            # Edit button
                            edit_key = f"edit_doctor_{doctor['email']}"
                            if edit_key not in st.session_state:
                                st.session_state[edit_key] = False
                            
                            if st.button("✏️ Edit", key=f"btn_edit_{doctor['email']}", use_container_width=True):
                                st.session_state[edit_key] = not st.session_state[edit_key]
                                st.rerun()
                        
                        with col2:
                            # Reset Password button
                            reset_key = f"reset_{doctor['email']}"
                            if reset_key not in st.session_state:
                                st.session_state[reset_key] = False
                            
                            if st.button("🔑 Reset Password", key=f"btn_reset_{doctor['email']}", use_container_width=True):
                                st.session_state[reset_key] = not st.session_state[reset_key]
                                st.rerun()
                        
                        with col3:
                            # Delete button
                            delete_key = f"delete_doctor_{doctor['email']}"
                            if delete_key not in st.session_state:
                                st.session_state[delete_key] = False
                            
                            if not st.session_state[delete_key]:
                                if st.button("🗑️ Delete", key=f"btn_delete_{doctor['email']}", use_container_width=True):
                                    st.session_state[delete_key] = True
                                    st.rerun()
                            else:
                                st.warning("⚠️ Are you sure?")
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("✅ Yes", key=f"confirm_delete_{doctor['email']}"):
                                        try:
                                            result = delete_doctor(doctor['email'])
                                            st.success("✅ Doctor deleted!")
                                            st.session_state[delete_key] = False
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Error: {e}")
                                with col_b:
                                    if st.button("❌ No", key=f"cancel_delete_{doctor['email']}"):
                                        st.session_state[delete_key] = False
                                        st.rerun()
                        
                        # Reset Password Form
                        if st.session_state.get(reset_key, False):
                            st.markdown("---")
                            st.markdown("##### 🔑 Reset Password")
                            new_pwd = st.text_input("New Password", type="password", key=f"new_pwd_c_{doctor['email']}")
                            confirm_pwd = st.text_input("Confirm Password", type="password", key=f"confirm_pwd_c_{doctor['email']}")
                            
                            col_r1, col_r2 = st.columns(2)
                            with col_r1:
                                if st.button("✅ Update", key=f"submit_reset_c_{doctor['email']}", use_container_width=True):
                                    if new_pwd != confirm_pwd:
                                        st.error("❌ Passwords do not match!")
                                    elif len(new_pwd) < 6:
                                        st.error("❌ Password must be at least 6 characters!")
                                    else:
                                        try:
                                            response = requests.put(
                                                f"{API_URL}/doctors/{doctor['email']}/password",
                                                json={"password": new_pwd}
                                            )
                                            if response.status_code == 200:
                                                st.success(f"✅ Password updated!")
                                                st.session_state[reset_key] = False
                                                st.rerun()
                                            else:
                                                st.error("❌ Failed")
                                        except Exception as e:
                                            st.error(f"❌ Error: {e}")
                            with col_r2:
                                if st.button("❌ Cancel", key=f"cancel_reset_c_{doctor['email']}", use_container_width=True):
                                    st.session_state[reset_key] = False
                                    st.rerun()
                        
                        # Edit form
                        if st.session_state.get(edit_key, False):
                            st.markdown("---")
                            st.subheader("Edit Cardiologist Information")
                            
                            with st.form(f"edit_form_{doctor['email']}"):
                                edit_name = st.text_input("Full Name *", value=doctor['name'])
                                edit_email = st.text_input("Email *", value=doctor['email'])
                                edit_hospital = st.text_input("Hospital/Clinic *", value=doctor['hospital_clinic'])
                                edit_ic = st.text_input("IC/Passport *", value=doctor['ic_passport'])
                                edit_mmc = st.text_input("MMC No. *", value=doctor.get('mmc_number', ''))
                                edit_nsr = st.text_input("NSR No. *", value=doctor.get('nsr_number', ''))
                                
                                if st.form_submit_button("💾 Save Changes", type="primary"):
                                    if edit_name and edit_email and edit_hospital and edit_ic and edit_mmc and edit_nsr:
                                        try:
                                            result = update_doctor(
                                                doctor['email'],
                                                edit_name,
                                                edit_email,
                                                "cardiologist",
                                                edit_hospital,
                                                edit_ic,
                                                edit_mmc,
                                                edit_nsr
                                            )
                                            st.success("✅ Cardiologist updated successfully!")
                                            st.session_state[edit_key] = False
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Error: {e}")
                                    else:
                                        st.warning("⚠️ Please fill in all required fields")
            else:
                st.info("No cardiologists found")
            
            # GP CLINICIANS SECTION
            st.markdown("---")
            st.subheader("🩺 GP Clinicians")
            
            if search_email:
                filtered_gp = [d for d in gp_clinicians if search_email.lower() in d['email'].lower()]
            else:
                filtered_gp = gp_clinicians
            
            if filtered_gp:
                for doctor in filtered_gp:
                    with st.expander(f"🩺 {doctor['name']} ({doctor['email']})"):
                        # Display current info
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Name:** {doctor['name']}")
                            st.write(f"**Email:** {doctor['email']}")
                            st.write(f"**Hospital/Clinic:** {doctor['hospital_clinic']}")
                        
                        with col2:
                            st.write(f"**IC/Passport:** {doctor['ic_passport']}")
                            st.write(f"**MMC No:** {doctor.get('mmc_number', 'N/A')}")
                        
                        st.markdown("---")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns([1, 1, 1])
                        
                        with col1:
                            # Edit button
                            edit_key = f"edit_doctor_{doctor['email']}"
                            if edit_key not in st.session_state:
                                st.session_state[edit_key] = False
                            
                            if st.button("✏️ Edit", key=f"btn_edit_{doctor['email']}", use_container_width=True):
                                st.session_state[edit_key] = not st.session_state[edit_key]
                                st.rerun()
                        
                        with col2:
                            # Reset Password button
                            reset_key = f"reset_{doctor['email']}"
                            if reset_key not in st.session_state:
                                st.session_state[reset_key] = False
                            
                            if st.button("🔑 Reset Password", key=f"btn_reset_{doctor['email']}", use_container_width=True):
                                st.session_state[reset_key] = not st.session_state[reset_key]
                                st.rerun()
                        
                        with col3:
                            # Delete button
                            delete_key = f"delete_doctor_{doctor['email']}"
                            if delete_key not in st.session_state:
                                st.session_state[delete_key] = False
                            
                            if not st.session_state[delete_key]:
                                if st.button("🗑️ Delete", key=f"btn_delete_{doctor['email']}", use_container_width=True):
                                    st.session_state[delete_key] = True
                                    st.rerun()
                            else:
                                st.warning("⚠️ Are you sure?")
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("✅ Yes", key=f"confirm_delete_{doctor['email']}"):
                                        try:
                                            result = delete_doctor(doctor['email'])
                                            st.success("✅ Doctor deleted!")
                                            st.session_state[delete_key] = False
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Error: {e}")
                                with col_b:
                                    if st.button("❌ No", key=f"cancel_delete_{doctor['email']}"):
                                        st.session_state[delete_key] = False
                                        st.rerun()
                        
                        # Reset Password Form
                        if st.session_state.get(reset_key, False):
                            st.markdown("---")
                            st.markdown("##### 🔑 Reset Password")
                            new_pwd = st.text_input("New Password", type="password", key=f"new_pwd_gp_{doctor['email']}")
                            confirm_pwd = st.text_input("Confirm Password", type="password", key=f"confirm_pwd_gp_{doctor['email']}")
                            
                            col_r1, col_r2 = st.columns(2)
                            with col_r1:
                                if st.button("✅ Update", key=f"submit_reset_gp_{doctor['email']}", use_container_width=True):
                                    if new_pwd != confirm_pwd:
                                        st.error("❌ Passwords do not match!")
                                    elif len(new_pwd) < 6:
                                        st.error("❌ Password must be at least 6 characters!")
                                    else:
                                        try:
                                            response = requests.put(
                                                f"{API_URL}/doctors/{doctor['email']}/password",
                                                json={"password": new_pwd}
                                            )
                                            if response.status_code == 200:
                                                st.success(f"✅ Password updated!")
                                                st.session_state[reset_key] = False
                                                st.rerun()
                                            else:
                                                st.error("❌ Failed")
                                        except Exception as e:
                                            st.error(f"❌ Error: {e}")
                            with col_r2:
                                if st.button("❌ Cancel", key=f"cancel_reset_gp_{doctor['email']}", use_container_width=True):
                                    st.session_state[reset_key] = False
                                    st.rerun()
                        
                        # Edit form
                        if st.session_state.get(edit_key, False):
                            st.markdown("---")
                            st.subheader("Edit GP Clinician Information")
                            
                            with st.form(f"edit_form_{doctor['email']}"):
                                edit_name = st.text_input("Full Name *", value=doctor['name'])
                                edit_email = st.text_input("Email *", value=doctor['email'])
                                edit_hospital = st.text_input("Hospital/Clinic *", value=doctor['hospital_clinic'])
                                edit_ic = st.text_input("IC/Passport *", value=doctor['ic_passport'])
                                edit_mmc = st.text_input("MMC No. *", value=doctor.get('mmc_number', ''))
                                
                                if st.form_submit_button("💾 Save Changes", type="primary"):
                                    if edit_name and edit_email and edit_hospital and edit_ic and edit_mmc:
                                        try:
                                            result = update_doctor(
                                                doctor['email'],
                                                edit_name,
                                                edit_email,
                                                "clinic_doctor",
                                                edit_hospital,
                                                edit_ic,
                                                edit_mmc,
                                                None
                                            )
                                            st.success("✅ GP Clinician updated successfully!")
                                            st.session_state[edit_key] = False
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Error: {e}")
                                    else:
                                        st.warning("⚠️ Please fill in all required fields")
            else:
                st.info("No GP Clinicians found")
        else:
            st.info("No doctors registered yet")
    
    except Exception as e:
        st.error(f"❌ Error loading doctors: {e}")

# ============= NEW CONSULTATION =============

elif page_clean == "➕ New Consultation":
    st.header("Create New Consultation Request")
    
    # Auto-use logged-in user's email
    clinic_doctor_email = st.session_state.user['email']
    user_role = st.session_state.user['role']
    
    # Show GP info
    st.info(f"**Creating consultation as:** {st.session_state.user['name']} ({clinic_doctor_email})")
    
    # Only GP Clinicians and Admin can create consultations
    if user_role not in ['clinic_doctor', 'admin']:
        st.error("❌ Only GP Clinicians and Administrators can create consultations.")
        st.stop()
    
    # File uploaders MUST be outside form
    st.subheader("📎 Medical Images (Optional)")
    st.markdown("*Upload ECG and/or X-Ray images before filling the form*")
    col1, col2 = st.columns(2)
    with col1:
        ecg_file = st.file_uploader("Upload ECG Image", type=["jpg", "jpeg", "png", "pdf"], key="ecg_uploader")
        if ecg_file:
            st.image(ecg_file, caption="ECG Preview", use_column_width=True)
    with col2:
        xray_file = st.file_uploader("Upload X-Ray Image", type=["jpg", "jpeg", "png", "pdf"], key="xray_uploader")
        if xray_file:
            st.image(xray_file, caption="X-Ray Preview", use_column_width=True)
    
    st.markdown("---")
    
    with st.form("consultation_form"):
        st.subheader("Patient Information")
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.text_input("Patient Name")
            patient_age = st.number_input("Age", min_value=0, max_value=120)
        with col2:
            patient_gender = st.selectbox("Gender", ["Male", "Female"])
            patient_ic = st.text_input("IC/Passport No")
        
        st.markdown("---")
        
        st.subheader("Clinical Information")
        symptoms = st.text_area("Symptoms", height=100)
        
        st.markdown("---")
        
        st.subheader("Vital Signs")
        col1, col2, col3 = st.columns(3)
        with col1:
            bp = st.text_input("Blood Pressure (e.g., 120/80)")
            hr = st.number_input("Heart Rate (bpm)", min_value=0)
        with col2:
            temp = st.number_input("Temperature (°C)", min_value=35.0, max_value=42.0, value=37.0)
            spo2 = st.number_input("SpO2 (%)", min_value=0, max_value=100)
        with col3:
            rr = st.number_input("Respiratory Rate", min_value=0)
        
        st.markdown("---")
        
        st.subheader("🧪 Lab Investigations (Optional)")
        st.markdown("*Enter lab test results - one per line in format: Test Name | Date Time | Result*")
        st.markdown("*Example: FBC | 2024-01-15 09:30 | WBC 12.5, RBC 4.8*")
        lab_investigations_text = st.text_area(
            "Lab Test Results",
            height=100,
            placeholder="FBC | 2024-01-15 09:30 | WBC 12.5, RBC 4.8\nLipid Profile | 2024-01-15 10:00 | Total Chol 6.2, LDL 4.1\nTroponin | 2024-01-15 11:00 | 0.05 ng/mL",
            help="Enter each test on a new line"
        )
        
        lab_remarks = st.text_area(
            "Remarks on Lab Results (Optional)",
            height=80,
            placeholder="e.g., Patient fasting for lipid profile. Troponin slightly elevated, repeat in 3 hours recommended.",
            help="Add any important notes about the lab investigations"
        )
        
        st.markdown("---")
        
        image_remarks = st.text_area(
            "Remarks on Images (Optional)",
            height=80,
            placeholder="e.g., ECG shows possible ST elevation in leads II, III, aVF. X-Ray taken in PA view, patient cooperative.",
            help="Add any important observations or context about the medical images"
        )
        
        st.markdown("---")
        
        st.subheader("🩺 Provisional Diagnosis")
        provisional_diagnosis = st.text_area(
            "Your Provisional Diagnosis",
            height=100,
            placeholder="e.g., Suspected acute coronary syndrome with possible inferior STEMI. Patient presenting with typical cardiac chest pain and risk factors.",
            help="Enter your initial clinical diagnosis based on the assessment"
        )
        
        st.markdown("---")
        
        st.subheader("Assignment & Priority")
        
        # Get list of cardiologists
        try:
            all_doctors = get_all_doctors()
            cardiologists = [d for d in all_doctors if d['role'] == 'cardiologist']
            cardio_options = ["Any Available Cardiologist"] + [f"{c['name']} ({c['hospital_clinic']})" for c in cardiologists]
            cardio_emails = [None] + [c['email'] for c in cardiologists]
            
            selected_cardio_index = st.selectbox(
                "Assign to Cardiologist",
                range(len(cardio_options)),
                format_func=lambda i: cardio_options[i],
                help="Select a specific Cardiologist or leave as 'Any Available' for open assignment"
            )
            assigned_cardiologist_email = cardio_emails[selected_cardio_index]
            
            if assigned_cardiologist_email:
                st.info(f"✅ This case will be assigned to: **{cardio_options[selected_cardio_index]}**")
        except:
            assigned_cardiologist_email = None
            st.warning("⚠️ Could not load Cardiologists list. Case will be unassigned.")
        
        urgency = st.selectbox(
            "Urgency Level",
            options=["normal", "urgent", "emergency"],
            format_func=lambda x: {"normal": "🟢 Normal", "urgent": "🟡 Urgent", "emergency": "🔴 Emergency"}[x],
            help="Normal: Non-urgent case; Urgent: Requires attention within 24-48 hours; Emergency: Immediate attention required"
        )
        
        submit = st.form_submit_button("Submit Consultation Request")
        
        if submit:
            if patient_name and symptoms:
                # Proceed with consultation creation
                try:
                    patient_data = {
                        "name": patient_name,
                        "age": patient_age,
                        "gender": patient_gender,
                        "ic_number": patient_ic
                    }
                    
                    vital_signs = {
                        "blood_pressure": bp,
                        "heart_rate": hr,
                        "temperature": temp,
                        "spo2": spo2,
                        "respiratory_rate": rr
                    }
                    
                    # Parse lab investigations from text
                    lab_tests = []
                    if lab_investigations_text:
                        for line in lab_investigations_text.strip().split('\n'):
                            if '|' in line:
                                parts = [p.strip() for p in line.split('|')]
                                if len(parts) >= 3:
                                    lab_tests.append({
                                        "test_name": parts[0],
                                        "date_time": parts[1],
                                        "result": parts[2]
                                    })
                    
                    # Sort lab tests by date descending
                    lab_tests.sort(key=lambda x: x['date_time'], reverse=True)
                    
                    result = create_consultation(
                        patient_data,
                        symptoms,
                        vital_signs,
                        clinic_doctor_email,
                        urgency,
                        assigned_cardiologist_email,
                        lab_tests,
                        lab_remarks,
                        image_remarks,
                        provisional_diagnosis
                    )
                    
                    # Handle response
                    if 'consultation_id' in result:
                        consultation_id = result['consultation_id']
                        st.success(f"✅ Consultation created successfully!")
                        st.info(f"Consultation ID: {consultation_id}")
                    else:
                        st.error(f"❌ Error creating consultation: {result.get('detail', 'Unknown error')}")
                        consultation_id = None
                    
                    # Upload images if provided
                    if consultation_id and ecg_file:
                        try:
                            ecg_result = upload_ecg(consultation_id, ecg_file)
                            st.success(f"📎 ECG image uploaded: {ecg_result['filename']}")
                            
                            # Auto-run AI analysis
                            with st.spinner("🤖 Running AI analysis on ECG..."):
                                try:
                                    ai_response = requests.post(
                                        f"{API_URL}/consultations/{consultation_id}/analyze-image",
                                        params={"image_type": "ecg"}
                                    )
                                    if ai_response.status_code == 200:
                                        ai_result = ai_response.json()
                                        st.success("✅ AI analysis completed!")
                                        with st.expander("🤖 View ECG Analysis", expanded=True):
                                            st.info(ai_result.get('analysis', 'Analysis completed'))
                                    else:
                                        st.warning(f"⚠️ AI analysis skipped: {ai_response.text}")
                                except Exception as ai_error:
                                    st.warning(f"⚠️ AI analysis failed: {ai_error}")
                        except Exception as e:
                            st.warning(f"⚠️ ECG upload failed: {e}")
                    
                    if consultation_id and xray_file:
                        try:
                            xray_result = upload_xray(consultation_id, xray_file)
                            st.success(f"📎 X-Ray image uploaded: {xray_result['filename']}")
                            
                            # Auto-run AI analysis
                            with st.spinner("🤖 Running AI analysis on X-Ray..."):
                                try:
                                    ai_response = requests.post(
                                        f"{API_URL}/consultations/{consultation_id}/analyze-image",
                                        params={"image_type": "xray"}
                                    )
                                    if ai_response.status_code == 200:
                                        ai_result = ai_response.json()
                                        st.success("✅ AI analysis completed!")
                                        with st.expander("🤖 View X-Ray Analysis", expanded=True):
                                            st.info(ai_result.get('analysis', 'Analysis completed'))
                                    else:
                                        st.warning(f"⚠️ AI analysis skipped: {ai_response.text}")
                                except Exception as ai_error:
                                    st.warning(f"⚠️ AI analysis failed: {ai_error}")
                        except Exception as e:
                            st.warning(f"⚠️ X-Ray upload failed: {e}")
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("Please fill in all required fields")

# ============= VIEW CONSULTATIONS =============

elif page_clean == "📋 View My Consultations" or page_clean == "📋 View My Responses":
    user_email = st.session_state.user['email']
    user_role = st.session_state.user['role']
    
    if page_clean == "📋 View My Consultations":
        st.header("My Consultations")
        st.markdown(f"**GP Clinician:** {st.session_state.user['name']}")
    else:
        st.header("My Responses")
        st.markdown(f"**Cardiologist:** {st.session_state.user['name']}")
    
    status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Reviewed", "Completed"])
    # Map display values back to API values
    status_map = {"All": None, "Pending": "pending", "Reviewed": "reviewed", "Completed": "completed"}
    status_value = status_map[status_filter]
    
    try:
        # Get all consultations
        all_consultations = get_consultations(status_value)
        
        # Filter by user (admin sees all)
        if user_role == 'admin':
            # Admin sees all consultations
            consultations = all_consultations
        elif user_role == 'clinic_doctor':
            # GP sees only consultations they created
            consultations = [c for c in all_consultations if c['clinic_doctor_email'] == user_email]
        else:  # cardiologist
            # Cardiologist sees only consultations they responded to
            consultations = [c for c in all_consultations if c.get('cardiologist_email') == user_email]
        
        if consultations:
            # Initialize session state for selected consultations
            if 'selected_consultations' not in st.session_state:
                st.session_state.selected_consultations = []
            
            # Bulk delete controls at top
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**Total: {len(consultations)} consultations**")
            with col2:
                select_all = st.checkbox("Select All", key="select_all_consultations")
                if select_all:
                    st.session_state.selected_consultations = [c['consultation_id'] for c in consultations]
                elif not select_all and len(st.session_state.selected_consultations) == len(consultations):
                    st.session_state.selected_consultations = []
            with col3:
                if len(st.session_state.selected_consultations) > 0:
                    if st.button(f"🗑️ Delete ({len(st.session_state.selected_consultations)})", type="primary", key="bulk_delete_btn"):
                        st.session_state.confirm_bulk_delete = True
            
            # Bulk delete confirmation
            if st.session_state.get('confirm_bulk_delete', False):
                st.warning(f"⚠️ Are you sure you want to delete {len(st.session_state.selected_consultations)} consultation(s)?")
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button("✅ Yes, Delete All", type="primary", key="confirm_bulk_yes"):
                        deleted_count = 0
                        for consultation_id in st.session_state.selected_consultations:
                            try:
                                response = requests.delete(f"{API_URL}/consultations/{consultation_id}")
                                if response.status_code == 200:
                                    deleted_count += 1
                            except:
                                pass
                        st.success(f"✅ Deleted {deleted_count} consultation(s)!")
                        st.session_state.selected_consultations = []
                        st.session_state.confirm_bulk_delete = False
                        st.rerun()
                with col2:
                    if st.button("❌ Cancel", key="confirm_bulk_no"):
                        st.session_state.confirm_bulk_delete = False
                        st.rerun()
            
            st.markdown("---")
            
            # Display consultations
            for consult in consultations:
                # Checkbox for selection
                is_selected = consult['consultation_id'] in st.session_state.selected_consultations
                
                with st.expander(f"{'☑️' if is_selected else '☐'} {consult['consultation_id']} - {consult['patient']['name']} ({consult['status'].upper()})"):
                    # Checkbox to select this consultation
                    selected = st.checkbox(
                        "Select for deletion",
                        value=is_selected,
                        key=f"select_{consult['consultation_id']}"
                    )
                    if selected and consult['consultation_id'] not in st.session_state.selected_consultations:
                        st.session_state.selected_consultations.append(consult['consultation_id'])
                    elif not selected and consult['consultation_id'] in st.session_state.selected_consultations:
                        st.session_state.selected_consultations.remove(consult['consultation_id'])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Patient Information:**")
                        st.write(f"Name: {consult['patient']['name']}")
                        st.write(f"Age: {consult['patient']['age']}")
                        st.write(f"Gender: {consult['patient']['gender']}")
                        st.write(f"IC: {consult['patient']['ic_number']}")
                        
                        # Display medical images if available
                        if consult['patient'].get('ecg_image'):
                            st.markdown("**📊 ECG Image:**")
                            st.image(f"http://localhost:8000/uploads/{consult['patient']['ecg_image']}", 
                                   caption="ECG", width=400)
                            
                            # AI Analysis button
                            col_btn1, col_btn2 = st.columns([1, 3])
                            with col_btn1:
                                if st.button("🤖 AI Analyze", key=f"analyze_ecg_{consult['consultation_id']}"):
                                    with st.spinner("🔄 Analyzing ECG..."):
                                        try:
                                            response = requests.post(
                                                f"{API_URL}/consultations/{consult['consultation_id']}/analyze-image",
                                                params={"image_type": "ecg"}
                                            )
                                            if response.status_code == 200:
                                                result = response.json()
                                                st.success("✅ Analysis complete!")
                                                st.rerun()
                                            else:
                                                st.error(f"❌ {response.json().get('detail', 'Error')}")
                                        except Exception as e:
                                            st.error(f"❌ Error: {e}")
                            
                            # Display existing analysis if available
                            if consult.get('ecg_analysis'):
                                st.info(f"**📋 AI Analysis:**\n\n{consult['ecg_analysis']}")
                        
                        if consult['patient'].get('xray_image'):
                            st.markdown("**🩻 X-Ray Image:**")
                            st.image(f"http://localhost:8000/uploads/{consult['patient']['xray_image']}", 
                                   caption="X-Ray", width=400)
                            
                            # AI Analysis button
                            col_btn1, col_btn2 = st.columns([1, 3])
                            with col_btn1:
                                if st.button("🤖 AI Analyze", key=f"analyze_xray_{consult['consultation_id']}"):
                                    with st.spinner("🔄 Analyzing X-Ray..."):
                                        try:
                                            response = requests.post(
                                                f"{API_URL}/consultations/{consult['consultation_id']}/analyze-image",
                                                params={"image_type": "xray"}
                                            )
                                            if response.status_code == 200:
                                                result = response.json()
                                                st.success("✅ Analysis complete!")
                                                st.rerun()
                                            else:
                                                st.error(f"❌ {response.json().get('detail', 'Error')}")
                                        except Exception as e:
                                            st.error(f"❌ Error: {e}")
                            
                            # Display existing analysis if available
                            if consult.get('xray_analysis'):
                                st.info(f"**📋 AI Analysis:**\n\n{consult['xray_analysis']}")
                        
                        st.markdown("**Clinic Doctor:**")
                        st.write(f"{consult['clinic_doctor_name']}")
                        st.write(f"{consult['clinic_doctor_email']}")
                    
                    with col2:
                        st.markdown("**Vital Signs:**")
                        st.write(f"BP: {consult['vital_signs'].get('blood_pressure', 'N/A')}")
                        st.write(f"HR: {consult['vital_signs'].get('heart_rate', 'N/A')} bpm")
                        st.write(f"Temp: {consult['vital_signs'].get('temperature', 'N/A')}°C")
                        st.write(f"SpO2: {consult['vital_signs'].get('spo2', 'N/A')}%")
                        
                        st.markdown(f"**Urgency:** ⚠️ {consult['urgency'].upper()}")
                        
                        # Show assignment info
                        if consult.get('assigned_cardiologist_email'):
                            st.markdown(f"**🎯 Assigned to:** {consult.get('assigned_cardiologist_name', 'N/A')}")
                            st.write(f"📧 {consult['assigned_cardiologist_email']}")
                        else:
                            st.markdown("**🎯 Assignment:** Any Available Cardiologist")
                    
                    st.markdown("**Symptoms:**")
                    st.write(consult['symptoms'])
                    
                    # Display GP's Provisional Diagnosis if available
                    if consult.get('provisional_diagnosis'):
                        st.markdown("---")
                        st.markdown("**🩺 GP's Provisional Diagnosis:**")
                        st.warning(consult['provisional_diagnosis'])
                    
                    # Display Lab Investigations if available
                    if consult.get('lab_investigations') and len(consult['lab_investigations']) > 0:
                        st.markdown("---")
                        st.markdown("**🧪 Lab Investigations:**")
                        # Sort by date descending
                        sorted_labs = sorted(consult['lab_investigations'], key=lambda x: x['date_time'], reverse=True)
                        
                        # Create table header
                        col1, col2, col3 = st.columns([3, 2, 3])
                        with col1:
                            st.markdown("**Test Name**")
                        with col2:
                            st.markdown("**Date & Time**")
                        with col3:
                            st.markdown("**Result**")
                        
                        st.markdown("---")
                        
                        # Display each lab test
                        for lab in sorted_labs:
                            col1, col2, col3 = st.columns([3, 2, 3])
                            with col1:
                                st.write(lab['test_name'])
                            with col2:
                                st.write(lab['date_time'])
                            with col3:
                                st.write(lab['result'])
                        
                        # Display GP's Lab Remarks if available
                        if consult.get('lab_remarks'):
                            st.markdown("**💬 GP's Remarks on Lab Results:**")
                            st.info(consult['lab_remarks'])
                    
                    # Display GP's Image Remarks if available
                    if consult.get('image_remarks') and (consult['patient'].get('ecg_image') or consult['patient'].get('xray_image')):
                        st.markdown("---")
                        st.markdown("**💬 GP's Remarks on Images:**")
                        st.info(consult['image_remarks'])
                    
                    if consult['status'] in ['reviewed', 'completed']:
                        st.markdown("---")
                        st.markdown("**Cardiologist Response:**")
                        st.write(f"👨‍⚕️ {consult.get('cardiologist_name', 'N/A')}")
                        st.write(f"📧 {consult.get('cardiologist_email', 'N/A')}")
                        st.markdown(f"**Diagnosis:** {consult.get('diagnosis', 'N/A')}")
                        st.markdown(f"**Recommendations:** {consult.get('recommendations', 'N/A')}")
                        st.markdown(f"**Notes:** {consult.get('cardiologist_notes', 'N/A')}")
                        
                        # GP Decision for reviewed consultations
                        if consult['status'] == 'reviewed':
                            st.markdown("---")
                            st.info("💡 **GP Decision Required:** Review the cardiologist's response and decide next action")
                            
                            # Complete consultation with confirmation
                            complete_key = f"confirm_complete_{consult['consultation_id']}"
                            if complete_key not in st.session_state:
                                st.session_state[complete_key] = False
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if not st.session_state[complete_key]:
                                    if st.button("✅ Complete Consultation", key=f"complete_{consult['consultation_id']}", type="primary", use_container_width=True):
                                        st.session_state[complete_key] = True
                                        st.rerun()
                                else:
                                    st.warning("⚠️ Are you sure you want to mark this consultation as completed?")
                                    col_a, col_b = st.columns(2)
                                    with col_a:
                                        if st.button("✅ Yes", key=f"yes_complete_{consult['consultation_id']}"):
                                            try:
                                                response = requests.put(f"{API_URL}/consultations/{consult['consultation_id']}/complete")
                                                if response.status_code == 200:
                                                    st.success("✅ Consultation marked as completed!")
                                                    st.session_state[complete_key] = False
                                                    st.rerun()
                                                else:
                                                    st.error("❌ Failed to complete consultation")
                                            except Exception as e:
                                                st.error(f"❌ Error: {e}")
                                    with col_b:
                                        if st.button("❌ No", key=f"no_complete_{consult['consultation_id']}"):
                                            st.session_state[complete_key] = False
                                            st.rerun()
                            
                            with col2:
                                continue_key = f"continue_{consult['consultation_id']}"
                                if continue_key not in st.session_state:
                                    st.session_state[continue_key] = False
                                
                                if st.button("🔄 Continue Discussion", key=f"btn_continue_{consult['consultation_id']}", use_container_width=True):
                                    st.session_state[continue_key] = not st.session_state[continue_key]
                                    st.rerun()
                            
                            # Show continue discussion form
                            if st.session_state.get(continue_key, False):
                                st.markdown("**📝 Add Follow-up Note:**")
                                with st.form(f"continue_form_{consult['consultation_id']}"):
                                    followup_note = st.text_area("Follow-up questions or additional information", height=100, placeholder="Add any questions or new information for the cardiologist...")
                                    
                                    if st.form_submit_button("📤 Send to Cardiologist"):
                                        if followup_note:
                                            # This would update the consultation with follow-up note
                                            # For now, just show success message
                                            st.info("💡 Feature in development: Follow-up notes will be sent to cardiologist for further review")
                                            st.session_state[continue_key] = False
                                        else:
                                            st.warning("⚠️ Please enter a follow-up note")
                    
                    # Actions section
                    st.markdown("---")
                    st.markdown("**Actions:**")
                    
                    # Action buttons in columns
                    action_cols = st.columns(3)
                    
                    # Edit button (only if pending)
                    if consult['status'] == 'pending':
                        with action_cols[0]:
                            edit_key = f"edit_mode_{consult['consultation_id']}"
                            if edit_key not in st.session_state:
                                st.session_state[edit_key] = False
                            
                            if st.button("📝 Edit" if not st.session_state[edit_key] else "❌ Cancel", 
                                        key=f"toggle_edit_{consult['consultation_id']}",
                                        use_container_width=True):
                                st.session_state[edit_key] = not st.session_state[edit_key]
                                st.rerun()
                    
                    # Delete button
                    with action_cols[1] if consult['status'] == 'pending' else action_cols[0]:
                        confirm_key = f"confirm_delete_{consult['consultation_id']}"
                        if confirm_key not in st.session_state:
                            st.session_state[confirm_key] = False
                        
                        if not st.session_state[confirm_key]:
                            if st.button("🗑️ Delete", key=f"delete_{consult['consultation_id']}", use_container_width=True):
                                st.session_state[confirm_key] = True
                                st.rerun()
                        else:
                            st.warning("⚠️ Are you sure?")
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✅ Yes", key=f"confirm_yes_{consult['consultation_id']}"):
                                    try:
                                        response = requests.delete(f"{API_URL}/consultations/{consult['consultation_id']}")
                                        if response.status_code == 200:
                                            st.success("✅ Deleted!")
                                            st.session_state[confirm_key] = False
                                            st.rerun()
                                        else:
                                            st.error(f"❌ Failed: {response.json().get('detail', 'Unknown error')}")
                                    except Exception as e:
                                        st.error(f"❌ Error: {e}")
                            with col2:
                                if st.button("❌ No", key=f"confirm_no_{consult['consultation_id']}"):
                                    st.session_state[confirm_key] = False
                                    st.rerun()
                    
                    # Show edit form if edit mode is active
                    if consult['status'] == 'pending':
                        edit_key = f"edit_mode_{consult['consultation_id']}"
                        if st.session_state.get(edit_key, False):
                            with st.form(f"edit_form_{consult['consultation_id']}"):
                                st.markdown("**Patient Information**")
                                edit_name = st.text_input("Patient Name", value=consult['patient']['name'])
                                col1, col2 = st.columns(2)
                                with col1:
                                    edit_age = st.number_input("Age", value=consult['patient']['age'], min_value=0, max_value=120)
                                    edit_gender = st.selectbox("Gender", ["Male", "Female"], index=0 if consult['patient']['gender'] == "Male" else 1)
                                with col2:
                                    edit_ic = st.text_input("IC/Passport No", value=consult['patient']['ic_number'])
                                
                                st.markdown("**Clinical Information**")
                                edit_symptoms = st.text_area("Symptoms", value=consult['symptoms'], height=100)
                                
                                st.markdown("**Vital Signs**")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    edit_bp = st.text_input("Blood Pressure", value=consult['vital_signs'].get('blood_pressure', ''))
                                    edit_hr = st.number_input("Heart Rate (bpm)", value=consult['vital_signs'].get('heart_rate', 0), min_value=0)
                                with col2:
                                    edit_temp = st.number_input("Temperature (°C)", value=float(consult['vital_signs'].get('temperature', 37.0)), min_value=35.0, max_value=42.0)
                                    edit_spo2 = st.number_input("SpO2 (%)", value=consult['vital_signs'].get('spo2', 0), min_value=0, max_value=100)
                                with col3:
                                    edit_rr = st.number_input("Respiratory Rate", value=consult['vital_signs'].get('respiratory_rate', 0), min_value=0)
                                
                                edit_urgency = st.selectbox(
                                    "Urgency Level",
                                    options=["normal", "urgent", "emergency"],
                                    index=["normal", "urgent", "emergency"].index(consult['urgency']),
                                    format_func=lambda x: {"normal": "🟢 Normal", "urgent": "🟡 Urgent", "emergency": "🔴 Emergency"}[x]
                                )
                                
                                st.markdown("**📎 Medical Images**")
                                
                                # Show current images status
                                col1, col2 = st.columns(2)
                                with col1:
                                    has_ecg = consult.get('ecg_image_url') is not None
                                    if has_ecg:
                                        st.info(f"✅ ECG image exists")
                                        remove_ecg = st.checkbox("Remove existing ECG", key=f"remove_ecg_{consult['consultation_id']}")
                                    else:
                                        st.info("ℹ️ No ECG uploaded")
                                        remove_ecg = False
                                    
                                    # Upload new ECG (replace or add new)
                                    new_ecg_file = st.file_uploader(
                                        "Upload ECG Image" + (" (replace)" if has_ecg else " (new)"),
                                        type=["jpg", "jpeg", "png", "pdf"],
                                        key=f"new_ecg_{consult['consultation_id']}"
                                    )
                                
                                with col2:
                                    has_xray = consult.get('xray_image_url') is not None
                                    if has_xray:
                                        st.info(f"✅ X-Ray image exists")
                                        remove_xray = st.checkbox("Remove existing X-Ray", key=f"remove_xray_{consult['consultation_id']}")
                                    else:
                                        st.info("ℹ️ No X-Ray uploaded")
                                        remove_xray = False
                                    
                                    # Upload new X-Ray (replace or add new)
                                    new_xray_file = st.file_uploader(
                                        "Upload X-Ray Image" + (" (replace)" if has_xray else " (new)"),
                                        type=["jpg", "jpeg", "png", "pdf"],
                                        key=f"new_xray_{consult['consultation_id']}"
                                    )
                                
                                if st.form_submit_button("💾 Save Changes", type="primary"):
                                    try:
                                        consultation_id = consult['consultation_id']
                                        update_data = {
                                            "patient": {
                                                "name": edit_name,
                                                "age": edit_age,
                                                "gender": edit_gender,
                                                "ic_number": edit_ic
                                            },
                                            "symptoms": edit_symptoms,
                                            "vital_signs": {
                                                "blood_pressure": edit_bp,
                                                "heart_rate": edit_hr,
                                                "temperature": edit_temp,
                                                "spo2": edit_spo2,
                                                "respiratory_rate": edit_rr
                                            },
                                            "urgency": edit_urgency,
                                            "clinic_doctor_email": consult['clinic_doctor_email']
                                        }
                                        
                                        # Handle image removals by setting to None
                                        if remove_ecg and has_ecg:
                                            update_data["ecg_image_url"] = None
                                        if remove_xray and has_xray:
                                            update_data["xray_image_url"] = None
                                        
                                        # Update consultation data (including image removals)
                                        response = requests.put(
                                            f"{API_URL}/consultations/{consultation_id}",
                                            json=update_data
                                        )
                                        
                                        if response.status_code == 200:
                                            success_messages = ["✅ Consultation data updated"]
                                            
                                            # Upload new ECG if provided
                                            if new_ecg_file is not None:
                                                try:
                                                    files = {"file": (new_ecg_file.name, new_ecg_file, new_ecg_file.type)}
                                                    ecg_response = requests.post(
                                                        f"{API_URL}/consultations/{consultation_id}/upload-ecg",
                                                        files=files
                                                    )
                                                    if ecg_response.status_code == 200:
                                                        success_messages.append("✅ ECG image uploaded")
                                                    else:
                                                        st.warning(f"⚠️ ECG upload failed: {ecg_response.json().get('detail', 'Unknown error')}")
                                                except Exception as e:
                                                    st.warning(f"⚠️ Could not upload ECG: {e}")
                                            
                                            # Upload new X-Ray if provided
                                            if new_xray_file is not None:
                                                try:
                                                    files = {"file": (new_xray_file.name, new_xray_file, new_xray_file.type)}
                                                    xray_response = requests.post(
                                                        f"{API_URL}/consultations/{consultation_id}/upload-xray",
                                                        files=files
                                                    )
                                                    if xray_response.status_code == 200:
                                                        success_messages.append("✅ X-Ray image uploaded")
                                                    else:
                                                        st.warning(f"⚠️ X-Ray upload failed: {xray_response.json().get('detail', 'Unknown error')}")
                                                except Exception as e:
                                                    st.warning(f"⚠️ Could not upload X-Ray: {e}")
                                            
                                            if remove_ecg and has_ecg:
                                                success_messages.append("✅ ECG image removed")
                                            if remove_xray and has_xray:
                                                success_messages.append("✅ X-Ray image removed")
                                            
                                            st.success(" | ".join(success_messages))
                                            st.session_state[edit_key] = False
                                            st.rerun()
                                        else:
                                            st.error(f"❌ Failed to update: {response.json().get('detail', 'Unknown error')}")
                                    except Exception as e:
                                        st.error(f"❌ Error: {e}")
                    
                    # Generate Referral Letter section
                    st.markdown("---")
                    st.markdown("**📄 Referral Letter:**")
                    referral_reason = st.text_input(
                        "Reason for Referral (Press Enter to update)",
                        value=f"Request for specialist cardiology opinion regarding {consult['symptoms'][:50]}...",
                        key=f"reason_{consult['consultation_id']}"
                    )
                    
                    include_images = st.checkbox(
                        "Include medical images (ECG/X-Ray) in PDF",
                        value=True,
                        key=f"img_{consult['consultation_id']}"
                    )
                    
                    if st.button("📄 Generate Referral Letter", key=f"ref_{consult['consultation_id']}", type="primary"):
                        try:
                            # Get GP doctor details
                            gp_email = consult['clinic_doctor_email']
                            gp_doctor_response = requests.get(f"{API_URL}/doctors/{gp_email}")
                            
                            if gp_doctor_response.status_code == 200:
                                gp_doctor = gp_doctor_response.json()
                                pdf_buffer = generate_referral_letter_pdf(consult, gp_doctor, referral_reason, include_images)
                                
                                st.download_button(
                                    label="💾 Download Referral Letter (PDF)",
                                    data=pdf_buffer,
                                    file_name=f"Referral_Letter_{consult['consultation_id']}_{consult['patient']['name'].replace(' ', '_')}.pdf",
                                    mime="application/pdf",
                                    key=f"download_{consult['consultation_id']}"
                                )
                                st.success("✅ Referral letter generated!")
                            else:
                                st.error("❌ Could not fetch GP doctor details")
                        except Exception as e:
                            st.error(f"❌ Error generating letter: {e}")
        else:
            st.info("No consultations found")
    except Exception as e:
        st.error(f"❌ Error loading consultations: {e}")

# ============= RESPOND TO CONSULTATION =============

elif page_clean == "💬 Respond to Consultation":
    st.header("Respond to Consultation (Cardiologist)")
    
    # Auto-use logged-in user's email
    cardiologist_email = st.session_state.user['email']
    user_role = st.session_state.user['role']
    
    # Show Cardiologist info
    st.info(f"**Responding as:** {st.session_state.user['name']} ({cardiologist_email})")
    
    # Only Cardiologists and Admin can respond
    if user_role not in ['cardiologist', 'admin']:
        st.error("❌ Only Cardiologists and Administrators can respond to consultations.")
        st.stop()
    
    try:
        pending_consultations = get_consultations("pending")
        
        if pending_consultations:
            # Separate assigned and unassigned cases
            assigned_to_me = [c for c in pending_consultations if c.get('assigned_cardiologist_email') == cardiologist_email]
            unassigned = [c for c in pending_consultations if not c.get('assigned_cardiologist_email')]
            assigned_to_others = [c for c in pending_consultations if c.get('assigned_cardiologist_email') and c.get('assigned_cardiologist_email') != cardiologist_email]
            
            # Show summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🔴 Assigned to You", len(assigned_to_me))
            with col2:
                st.metric("🔵 Unassigned (Available)", len(unassigned))
            with col3:
                st.metric("⚪ Assigned to Others", len(assigned_to_others))
            
            st.markdown("---")
            
            # Combine for display: assigned first (priority), then unassigned, then others
            all_cases = assigned_to_me + unassigned + assigned_to_others
            
            if all_cases:
                # Create consultation display with assignment info
                consultation_options = []
                for c in all_cases:
                    assignment_icon = ""
                    if c.get('assigned_cardiologist_email') == cardiologist_email:
                        assignment_icon = "🔴 "  # Assigned to me (priority)
                    elif not c.get('assigned_cardiologist_email'):
                        assignment_icon = "🔵 "  # Unassigned (available)
                    else:
                        assignment_icon = "⚪ "  # Assigned to someone else
                    
                    consultation_options.append(f"{assignment_icon}{c['consultation_id']} - {c['patient']['name']}")
                
                selected = st.selectbox("Select Consultation", consultation_options)
                
                if selected:
                    # Extract consultation ID (remove icon and split)
                    consultation_id = selected.split(" ")[1]  # Get CON-XXX part
                    selected_consult = next(c for c in all_cases if c['consultation_id'] == consultation_id)
                    
                    # Show assignment info
                    if selected_consult.get('assigned_cardiologist_email'):
                        if selected_consult['assigned_cardiologist_email'] == cardiologist_email:
                            st.success(f"✅ **This case is assigned to YOU**")
                        else:
                            st.warning(f"⚠️ **This case is assigned to:** {selected_consult.get('assigned_cardiologist_name', 'Another Cardiologist')}")
                            st.info("You can still respond if needed (will override assignment)")
                    else:
                        st.info("ℹ️ **This case is unassigned** - Available for any Cardiologist")
                    
                    st.markdown("---")
                    st.subheader("Consultation Details")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Patient Information:**")
                        st.write(f"**Patient:** {selected_consult['patient']['name']}")
                        st.write(f"**Age:** {selected_consult['patient']['age']}")
                        st.write(f"**Gender:** {selected_consult['patient']['gender']}")
                        st.write(f"**IC/Passport:** {selected_consult['patient']['ic_number']}")
                        
                        st.markdown("**Clinical Information:**")
                        st.write(f"**Symptoms:** {selected_consult['symptoms']}")
                        st.write(f"**Urgency:** {selected_consult['urgency'].upper()}")
                        
                    with col2:
                        st.markdown("**Vital Signs:**")
                        st.write(f"**BP:** {selected_consult['vital_signs'].get('blood_pressure')}")
                        st.write(f"**HR:** {selected_consult['vital_signs'].get('heart_rate')} bpm")
                        st.write(f"**Temperature:** {selected_consult['vital_signs'].get('temperature')}°C")
                        st.write(f"**SpO2:** {selected_consult['vital_signs'].get('spo2')}%")
                        st.write(f"**Respiratory Rate:** {selected_consult['vital_signs'].get('respiratory_rate')} /min")
                    
                    # Display Lab Investigations if available
                    if selected_consult.get('lab_investigations') and len(selected_consult['lab_investigations']) > 0:
                        st.markdown("---")
                        st.markdown("**🧪 Lab Investigations:**")
                        # Sort by date descending
                        sorted_labs = sorted(selected_consult['lab_investigations'], key=lambda x: x['date_time'], reverse=True)
                        
                        # Create table header
                        col1, col2, col3 = st.columns([3, 2, 3])
                        with col1:
                            st.markdown("**Test Name**")
                        with col2:
                            st.markdown("**Date & Time**")
                        with col3:
                            st.markdown("**Result**")
                        
                        st.markdown("---")
                        
                        # Display each lab test
                        for lab in sorted_labs:
                            col1, col2, col3 = st.columns([3, 2, 3])
                            with col1:
                                st.write(lab['test_name'])
                            with col2:
                                st.write(lab['date_time'])
                            with col3:
                                st.write(lab['result'])
                    
                    # Display GP's Lab Remarks if available
                    if selected_consult.get('lab_remarks'):
                        st.markdown("**💬 GP's Remarks on Lab Results:**")
                        st.info(selected_consult['lab_remarks'])
                    
                    # Display GP's Provisional Diagnosis if available
                    if selected_consult.get('provisional_diagnosis'):
                        st.markdown("---")
                        st.markdown("**🩺 GP's Provisional Diagnosis:**")
                        st.warning(selected_consult['provisional_diagnosis'])
                    
                    # Display Medical Images if available
                    if selected_consult['patient'].get('ecg_image') or selected_consult['patient'].get('xray_image'):
                        st.markdown("---")
                        st.markdown("**📊 Medical Images:**")
                        
                        # Display GP's Image Remarks if available
                        if selected_consult.get('image_remarks'):
                            st.markdown("**💬 GP's Remarks on Images:**")
                            st.info(selected_consult['image_remarks'])
                        
                        img_col1, img_col2 = st.columns(2)
                        
                        with img_col1:
                            if selected_consult['patient'].get('ecg_image'):
                                st.markdown("**ECG Image:**")
                                st.image(f"http://localhost:8000/uploads/{selected_consult['patient']['ecg_image']}", 
                                       caption="ECG", width=400)
                                
                                # Show AI analysis if available
                                if selected_consult.get('ecg_analysis'):
                                    st.info(f"**🤖 AI ECG Analysis:**\n\n{selected_consult['ecg_analysis']}")
                        
                        with img_col2:
                            if selected_consult['patient'].get('xray_image'):
                                st.markdown("**X-Ray Image:**")
                                st.image(f"http://localhost:8000/uploads/{selected_consult['patient']['xray_image']}", 
                                       caption="X-Ray", width=400)
                                
                                # Show AI analysis if available
                                if selected_consult.get('xray_analysis'):
                                    st.info(f"**🤖 AI X-Ray Analysis:**\n\n{selected_consult['xray_analysis']}")
                    
                    st.markdown("---")
                    st.subheader("Your Response")
                    
                    with st.form("response_form"):
                        diagnosis = st.text_area("Diagnosis", height=100)
                        recommendations = st.text_area("Recommendations", height=100)
                        notes = st.text_area("Additional Notes", height=100)
                        
                        submit = st.form_submit_button("Submit Response")
                        
                        if submit:
                            if diagnosis and recommendations:
                                # Proceed with response submission
                                try:
                                    result = respond_to_consultation(
                                        consultation_id,
                                        diagnosis,
                                        recommendations,
                                        notes,
                                        cardiologist_email
                                    )
                                    st.success("✅ Response submitted successfully!")
                                    st.rerun()  # Refresh page to show updated list
                                except Exception as e:
                                    st.error(f"❌ Error submitting response: {e}")
                            else:
                                st.warning("Please fill in all required fields")
            else:
                st.info("No pending consultations available")
        else:
            st.info("No pending consultations")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ============= STATISTICS =============

elif page_clean == "📊 Statistics" or page_clean == "📊 My Statistics":
    user_email = st.session_state.user['email']
    user_role = st.session_state.user['role']
    
    if page == "📊 My Statistics":
        st.header("My Statistics")
        if user_role == 'clinic_doctor':
            st.markdown(f"**GP Clinician:** {st.session_state.user['name']}")
        else:
            st.markdown(f"**Cardiologist:** {st.session_state.user['name']}")
    else:
        st.header("System Statistics")
    
    try:
        stats = get_stats()
        all_consultations = get_consultations()
        
        # Filter consultations by user if not admin
        if page == "📊 My Statistics":
            if user_role == 'clinic_doctor':
                my_consultations = [c for c in all_consultations if c['clinic_doctor_email'] == user_email]
            else:  # cardiologist
                my_consultations = [c for c in all_consultations if c.get('cardiologist_email') == user_email]
            
            # Calculate user-specific stats
            total_consultations = len(my_consultations)
            pending = len([c for c in my_consultations if c['status'] == 'pending'])
            reviewed = len([c for c in my_consultations if c['status'] == 'reviewed'])
            completed = len([c for c in my_consultations if c['status'] == 'completed'])
        else:
            # Admin or full statistics page sees all stats
            my_consultations = all_consultations
            total_consultations = stats["total_consultations"]
            pending = stats["pending"]
            reviewed = stats["reviewed"]
            completed = stats["completed"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Consultations", total_consultations)
            if page == "📊 Statistics":
                st.metric("Total Doctors", stats["total_doctors"])
        
        with col2:
            st.metric("Pending Consultations", pending)
            st.metric("Reviewed Consultations", reviewed)
            st.metric("Completed Consultations", completed)
        
        st.markdown("---")
        
        # Donut Charts
        import plotly.graph_objects as go
        import pandas as pd
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Consultation Status Distribution")
            # Donut chart for consultation status
            fig = go.Figure(data=[go.Pie(
                labels=['Pending', 'Reviewed', 'Completed'],
                values=[pending, reviewed, completed],
                hole=.5,
                marker_colors=['#FFA500', '#4169E1', '#32CD32']
            )])
            fig.update_layout(
                showlegend=True,
                height=400,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Statistics Table")
            # Data table
            table_rows = [
                {'Variable': 'Total Consultations', 'Count': total_consultations, 'Percentage': '100%'},
                {'Variable': 'Pending', 'Count': pending, 'Percentage': f"{(pending/total_consultations*100):.1f}%" if total_consultations > 0 else '0%'},
                {'Variable': 'Reviewed', 'Count': reviewed, 'Percentage': f"{(reviewed/total_consultations*100):.1f}%" if total_consultations > 0 else '0%'},
                {'Variable': 'Completed', 'Count': completed, 'Percentage': f"{(completed/total_consultations*100):.1f}%" if total_consultations > 0 else '0%'},
            ]
            
            if page == "📊 Statistics":
                table_rows.append({'Variable': 'Total Doctors', 'Count': stats["total_doctors"], 'Percentage': 'N/A'})
            
            table_data = pd.DataFrame(table_rows)
            st.dataframe(table_data, use_container_width=True, hide_index=True)
        
        # Patient File Reference Table
        st.markdown("---")
        st.subheader("Patient File References")
        
        try:
            if my_consultations:
                st.write("Click on Consultation ID to view patient details:")
                
                for consult in my_consultations:
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                    
                    with col1:
                        # Clickable button with consultation ID
                        if st.button(f"📁 {consult['consultation_id']}", key=f"view_{consult['consultation_id']}", use_container_width=True):
                            st.session_state.selected_patient = consult['consultation_id']
                    
                    with col2:
                        st.write(f"**{consult['patient']['name']}**")
                    
                    with col3:
                        st.write(f"{consult['patient']['ic_number']}")
                    
                    with col4:
                        status_color = {"pending": "🟡", "reviewed": "🔵", "completed": "🟢"}
                        st.write(f"{status_color.get(consult['status'], '⚪')} {consult['status'].upper()}")
                
                # Show selected patient details
                if 'selected_patient' in st.session_state:
                    selected_consult = next((c for c in all_consultations if c['consultation_id'] == st.session_state.selected_patient), None)
                    
                    if selected_consult:
                        st.markdown("---")
                        st.subheader(f"📋 Patient File: {st.session_state.selected_patient}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Patient Information:**")
                            st.write(f"Name: {selected_consult['patient']['name']}")
                            st.write(f"Age: {selected_consult['patient']['age']}")
                            st.write(f"Gender: {selected_consult['patient']['gender']}")
                            st.write(f"IC/Passport No: {selected_consult['patient']['ic_number']}")
                            
                            st.markdown("**Clinical Information:**")
                            st.write(f"**Symptoms:** {selected_consult['symptoms']}")
                            st.write(f"**Urgency:** {selected_consult['urgency'].upper()}")
                            st.write(f"**Status:** {selected_consult['status'].upper()}")
                            st.write(f"**Created:** {format_datetime(selected_consult.get('created_at', 'N/A'))}")
                        
                        with col2:
                            st.markdown("**Vital Signs:**")
                            vs = selected_consult['vital_signs']
                            st.write(f"Blood Pressure: {vs.get('blood_pressure', 'N/A')}")
                            st.write(f"Heart Rate: {vs.get('heart_rate', 'N/A')} bpm")
                            st.write(f"Temperature: {vs.get('temperature', 'N/A')}°C")
                            st.write(f"SpO2: {vs.get('spo2', 'N/A')}%")
                            st.write(f"Respiratory Rate: {vs.get('respiratory_rate', 'N/A')} /min")
                            
                            st.markdown("**GP Clinician:**")
                            st.write(f"Name: {selected_consult.get('clinic_doctor_name', 'N/A')}")
                            st.write(f"Email: {selected_consult.get('clinic_doctor_email', 'N/A')}")
                        
                        # Medical Images
                        if selected_consult['patient'].get('ecg_image') or selected_consult['patient'].get('xray_image'):
                            st.markdown("**Medical Images:**")
                            img_col1, img_col2 = st.columns(2)
                            with img_col1:
                                if selected_consult['patient'].get('ecg_image'):
                                    st.markdown("**📊 ECG Image:**")
                                    st.image(f"http://localhost:8000/uploads/{selected_consult['patient']['ecg_image']}", 
                                           caption="ECG", width=400)
                                    
                                    # AI Analysis button for ECG
                                    col_analyze, col_space = st.columns([1, 2])
                                    with col_analyze:
                                        if st.button("🤖 Analyze ECG", key="btn_analyze_ecg"):
                                            with st.spinner("🔄 Analyzing ECG image..."):
                                                response = requests.post(
                                                    f"{API_URL}/consultations/{selected_consult['consultation_id']}/analyze-image",
                                                    params={"image_type": "ecg"}
                                                )
                                                if response.status_code == 200:
                                                    result = response.json()
                                                    st.success("✅ Analysis complete!")
                                                    st.info(f"**AI ECG Analysis:**\n\n{result['analysis']}")
                                                else:
                                                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                                    
                                    # Display existing analysis if available
                                    if selected_consult.get('ecg_analysis'):
                                        st.markdown("---")
                                        st.markdown("**📋 ECG Analysis History:**")
                                        st.info(selected_consult['ecg_analysis'])
                                        
                            with img_col2:
                                if selected_consult['patient'].get('xray_image'):
                                    st.markdown("**🩻 X-Ray Image:**")
                                    st.image(f"http://localhost:8000/uploads/{selected_consult['patient']['xray_image']}", 
                                           caption="X-Ray", width=400)
                                    
                                    # AI Analysis button for X-Ray
                                    col_analyze, col_space = st.columns([1, 2])
                                    with col_analyze:
                                        if st.button("🤖 Analyze X-Ray", key="btn_analyze_xray"):
                                            with st.spinner("🔄 Analyzing X-Ray image..."):
                                                response = requests.post(
                                                    f"{API_URL}/consultations/{selected_consult['consultation_id']}/analyze-image",
                                                    params={"image_type": "xray"}
                                                )
                                                if response.status_code == 200:
                                                    result = response.json()
                                                    st.success("✅ Analysis complete!")
                                                    st.info(f"**AI X-Ray Analysis:**\n\n{result['analysis']}")
                                                else:
                                                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                                    
                                    # Display existing analysis if available
                                    if selected_consult.get('xray_analysis'):
                                        st.markdown("---")
                                        st.markdown("**📋 X-Ray Analysis History:**")
                                        st.info(selected_consult['xray_analysis'])
                        
                        # Cardiologist Response
                        if selected_consult['status'] in ['reviewed', 'completed']:
                            st.markdown("---")
                            st.markdown("**Cardiologist Response:**")
                            st.write(f"Cardiologist: {selected_consult.get('cardiologist_name', 'N/A')}")
                            st.write(f"Email: {selected_consult.get('cardiologist_email', 'N/A')}")
                            st.write(f"**Diagnosis:** {selected_consult.get('diagnosis', 'N/A')}")
                            st.write(f"**Recommendations:** {selected_consult.get('recommendations', 'N/A')}")
                            st.write(f"**Notes:** {selected_consult.get('cardiologist_notes', 'N/A')}")
                            st.write(f"**Response Date:** {format_datetime(selected_consult.get('response_date', 'N/A'))}")
                        
                        if st.button("❌ Close Patient File"):
                            del st.session_state.selected_patient
                            st.rerun()
            else:
                st.info("No patient records found")
        except Exception as e:
            st.warning(f"⚠️ Could not load patient references: {e}")
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
