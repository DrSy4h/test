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

def create_consultation(patient_data, symptoms, vital_signs, clinic_doctor_email, urgency):
    """Create new consultation"""
    payload = {
        "patient": patient_data,
        "symptoms": symptoms,
        "vital_signs": vital_signs,
        "clinic_doctor_email": clinic_doctor_email,
        "urgency": urgency
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
    
    # Reason for Referral
    if referral_reason:
        elements.append(Paragraph("<b>Reason for Referral:</b>", header_style))
        elements.append(Paragraph(referral_reason, normal_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Urgency
    elements.append(Paragraph(f"<b>Urgency Level:</b> {consultation['urgency'].upper()}", header_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Medical Images (if included)
    if include_images:
        patient = consultation['patient']
        if patient.get('ecg_image') or patient.get('xray_image'):
            elements.append(Paragraph("<b>Attached Medical Images:</b>", header_style))
            if patient.get('ecg_image'):
                elements.append(Paragraph(f"• ECG Image: {patient['ecg_image']}", normal_style))
            if patient.get('xray_image'):
                elements.append(Paragraph(f"• X-Ray Image: {patient['xray_image']}", normal_style))
            elements.append(Paragraph("<i>(Images available in digital consultation record)</i>", ParagraphStyle('small', parent=normal_style, fontSize=8, textColor=colors.grey)))
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

st.sidebar.markdown("### 📋 Navigation Menu")

# Navigation with radio buttons
page = st.sidebar.radio(
    "",
    ["🏠 Home", "👨‍⚕️ Register New Doctor", "👥 Manage Doctors", "➕ New Consultation", "💬 Respond to Consultation", "📋 View Consultations", "📊 Statistics"],
    label_visibility="collapsed"
)

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

# ============= HOME PAGE =============

if page == "🏠 Home":
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

elif page == "👨‍⚕️ Register New Doctor":
    st.header("Register New Doctor")
    
    name = st.text_input("Full Name *", help="Full name as per registration")
    email = st.text_input("Email *", help="Professional email address")
    role = st.selectbox("Role *", ["GP Clinician", "Cardiologist"], help="Select your role")
    hospital_clinic = st.text_input("Hospital/Clinic Name *", help="Current workplace")
    ic_passport = st.text_input("IC/Passport Number *", help="National ID or Passport number")
    mmc_number = st.text_input("MMC Full Registration No. *", help="Malaysian Medical Council registration number")
    
    # NSR number - compulsory for cardiologists, appears dynamically
    nsr_number = ""
    if role == "Cardiologist":
        nsr_number = st.text_input("NSR No. * (Compulsory for Cardiologists)", help="National Specialist Register number - Required for Cardiologists")
    
    if st.button("Register", type="primary"):
        # Validate all required fields
        if role == "Cardiologist":
            all_filled = name and email and hospital_clinic and ic_passport and mmc_number and nsr_number
            if not nsr_number:
                st.error("❌ NSR No. is compulsory for Cardiologists!")
        else:
            all_filled = name and email and hospital_clinic and ic_passport and mmc_number
        
        if all_filled:
            try:
                # Convert role display to backend format
                role_backend = "clinic_doctor" if role == "GP Clinician" else "cardiologist"
                result = register_doctor(name, email, role_backend, hospital_clinic, ic_passport, mmc_number, nsr_number if role == "Cardiologist" else None)
                st.success(f"✅ Doctor registered successfully!")
                st.json(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Please fill in all required fields (marked with *)")

# ============= MANAGE DOCTORS =============

elif page == "👥 Manage Doctors":
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
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            # Edit button
                            edit_key = f"edit_doctor_{doctor['email']}"
                            if edit_key not in st.session_state:
                                st.session_state[edit_key] = False
                            
                            if st.button("✏️ Edit", key=f"btn_edit_{doctor['email']}", use_container_width=True):
                                st.session_state[edit_key] = not st.session_state[edit_key]
                                st.rerun()
                        
                        with col2:
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
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            # Edit button
                            edit_key = f"edit_doctor_{doctor['email']}"
                            if edit_key not in st.session_state:
                                st.session_state[edit_key] = False
                            
                            if st.button("✏️ Edit", key=f"btn_edit_{doctor['email']}", use_container_width=True):
                                st.session_state[edit_key] = not st.session_state[edit_key]
                                st.rerun()
                        
                        with col2:
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

elif page == "➕ New Consultation":
    st.header("Create New Consultation Request")
    
    # Email validation outside form for immediate feedback
    st.subheader("GP Clinician Information")
    clinic_doctor_email = st.text_input("Your Email (GP Clinician)", key="gp_email_input")
    
    # Validate GP email in real-time
    gp_valid = False
    if clinic_doctor_email:
        try:
            doctor_check = requests.get(f"{API_URL}/doctors/{clinic_doctor_email}")
            if doctor_check.status_code != 200:
                st.error(f"❌ Email '{clinic_doctor_email}' not registered. Please register first.")
                st.info("💡 Go to 'Register New Doctor' page to register as GP Clinician.")
            else:
                doctor = doctor_check.json()
                if doctor.get('role') != 'clinic_doctor':
                    role_display = "Cardiologist" if doctor.get('role') == 'cardiologist' else doctor.get('role', 'Unknown')
                    st.error(f"❌ This email is registered as {role_display}. Only GP Clinicians can create consultations.")
                else:
                    st.success(f"✅ Verified: {doctor.get('name')} (GP Clinician)")
                    gp_valid = True
        except Exception as e:
            st.warning(f"⚠️ Unable to validate email: {e}")
    
    with st.form("consultation_form"):
        st.subheader("Patient Information")
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.text_input("Patient Name")
            patient_age = st.number_input("Age", min_value=0, max_value=120)
        with col2:
            patient_gender = st.selectbox("Gender", ["Male", "Female"])
            patient_ic = st.text_input("IC/Passport No")
        
        st.subheader("Clinical Information")
        symptoms = st.text_area("Symptoms", height=100)
        
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
        
        st.subheader("📎 Medical Images (Optional)")
        col1, col2 = st.columns(2)
        with col1:
            ecg_file = st.file_uploader("Upload ECG Image", type=["jpg", "jpeg", "png", "pdf"])
        with col2:
            xray_file = st.file_uploader("Upload X-Ray Image", type=["jpg", "jpeg", "png", "pdf"])
        
        urgency = st.selectbox(
            "Urgency Level",
            options=["normal", "urgent", "emergency"],
            format_func=lambda x: {"normal": "🟢 Normal", "urgent": "🟡 Urgent", "emergency": "🔴 Emergency"}[x]
        )
        
        submit = st.form_submit_button("Submit Consultation Request")
        
        if submit:
            if not gp_valid:
                st.error("❌ Please enter a valid GP Clinician email before submitting.")
            elif clinic_doctor_email and patient_name and symptoms:
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
                    
                    result = create_consultation(
                        patient_data,
                        symptoms,
                        vital_signs,
                        clinic_doctor_email,
                        urgency
                    )
                    
                    # Handle response
                    if 'consultation_id' in result:
                        consultation_id = result['consultation_id']
                        st.success(f"✅ Consultation created successfully!")
                        st.info(f"Consultation ID: {consultation_id}")
                    else:
                        st.error(f"❌ Error creating consultation: {result.get('detail', 'Unknown error')}")
                        st.json(result)
                        consultation_id = None
                    
                    # Upload images if provided
                    if consultation_id and ecg_file:
                        try:
                            ecg_result = upload_ecg(consultation_id, ecg_file)
                            st.success(f"📎 ECG image uploaded: {ecg_result['filename']}")
                        except Exception as e:
                            st.warning(f"⚠️ ECG upload failed: {e}")
                    
                    if consultation_id and xray_file:
                        try:
                            xray_result = upload_xray(consultation_id, xray_file)
                            st.success(f"📎 X-Ray image uploaded: {xray_result['filename']}")
                        except Exception as e:
                            st.warning(f"⚠️ X-Ray upload failed: {e}")
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("Please fill in all required fields")

# ============= VIEW CONSULTATIONS =============

elif page == "📋 View Consultations":
    st.header("View Consultations")
    
    status_filter = st.selectbox("Filter by Status", ["All", "pending", "reviewed", "completed"])
    
    try:
        consultations = get_consultations(status_filter if status_filter != "All" else None)
        
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
                        
                        if consult['patient'].get('xray_image'):
                            st.markdown("**🩻 X-Ray Image:**")
                            st.image(f"http://localhost:8000/uploads/{consult['patient']['xray_image']}", 
                                   caption="X-Ray", width=400)
                        
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
                    
                    st.markdown("**Symptoms:**")
                    st.write(consult['symptoms'])
                    
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

elif page == "💬 Respond to Consultation":
    st.header("Respond to Consultation (Cardiologist)")
    
    # Email validation outside form for immediate feedback
    cardiologist_email = st.text_input("Your Email (Cardiologist)", key="cardio_email_input")
    
    # Validate Cardiologist email in real-time
    cardio_valid = False
    if cardiologist_email:
        try:
            doctor_check = requests.get(f"{API_URL}/doctors/{cardiologist_email}")
            if doctor_check.status_code != 200:
                st.error(f"❌ Email '{cardiologist_email}' not registered. Please register first.")
                st.info("💡 Go to 'Register New Doctor' page to register as Cardiologist.")
            else:
                doctor = doctor_check.json()
                if doctor.get('role') != 'cardiologist':
                    role_display = "GP Clinician" if doctor.get('role') == 'clinic_doctor' else doctor.get('role', 'Unknown')
                    st.error(f"❌ This email is registered as {role_display}. Only Cardiologists can respond to consultations.")
                else:
                    st.success(f"✅ Verified: {doctor.get('name')} (Cardiologist)")
                    cardio_valid = True
        except Exception as e:
            st.warning(f"⚠️ Unable to validate email: {e}")
    
    try:
        pending_consultations = get_consultations("pending")
        
        if pending_consultations:
            consultation_ids = [f"{c['consultation_id']} - {c['patient']['name']}" for c in pending_consultations]
            selected = st.selectbox("Select Consultation", consultation_ids)
            
            if selected:
                consultation_id = selected.split(" - ")[0]
                selected_consult = next(c for c in pending_consultations if c['consultation_id'] == consultation_id)
                
                st.subheader("Consultation Details")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Patient:** {selected_consult['patient']['name']}")
                    st.write(f"**Age:** {selected_consult['patient']['age']}")
                    st.write(f"**Symptoms:** {selected_consult['symptoms']}")
                with col2:
                    st.write(f"**BP:** {selected_consult['vital_signs'].get('blood_pressure')}")
                    st.write(f"**HR:** {selected_consult['vital_signs'].get('heart_rate')} bpm")
                    st.write(f"**Urgency:** {selected_consult['urgency']}")
                
                st.markdown("---")
                st.subheader("Your Response")
                
                with st.form("response_form"):
                    diagnosis = st.text_area("Diagnosis", height=100)
                    recommendations = st.text_area("Recommendations", height=100)
                    notes = st.text_area("Additional Notes", height=100)
                    
                    submit = st.form_submit_button("Submit Response")
                    
                    if submit:
                        if not cardio_valid:
                            st.error("❌ Please enter a valid Cardiologist email before submitting.")
                        elif cardiologist_email and diagnosis and recommendations:
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
                                st.json(result)
                            except Exception as e:
                                st.error(f"❌ Error submitting response: {e}")
                        else:
                            st.warning("Please fill in all required fields")
        else:
            st.info("No pending consultations")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ============= STATISTICS =============

elif page == "📊 Statistics":
    st.header("System Statistics")
    
    try:
        stats = get_stats()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Consultations", stats["total_consultations"])
            st.metric("Total Doctors", stats["total_doctors"])
        
        with col2:
            st.metric("Pending Consultations", stats["pending"])
            st.metric("Reviewed Consultations", stats["reviewed"])
            st.metric("Completed Consultations", stats["completed"])
        
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
                values=[stats["pending"], stats["reviewed"], stats["completed"]],
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
            table_data = pd.DataFrame({
                'Variable': ['Total Consultations', 'Pending', 'Reviewed', 'Completed', 'Total Doctors'],
                'Count': [
                    stats["total_consultations"],
                    stats["pending"],
                    stats["reviewed"],
                    stats["completed"],
                    stats["total_doctors"]
                ],
                'Percentage': [
                    '100%',
                    f"{(stats['pending']/stats['total_consultations']*100):.1f}%" if stats['total_consultations'] > 0 else '0%',
                    f"{(stats['reviewed']/stats['total_consultations']*100):.1f}%" if stats['total_consultations'] > 0 else '0%',
                    f"{(stats['completed']/stats['total_consultations']*100):.1f}%" if stats['total_consultations'] > 0 else '0%',
                    'N/A'
                ]
            })
            st.dataframe(table_data, use_container_width=True, hide_index=True)
        
        # Patient File Reference Table
        st.markdown("---")
        st.subheader("Patient File References")
        
        try:
            # Get all consultations to show patient references
            all_consultations = get_consultations()
            if all_consultations:
                st.write("Click on Consultation ID to view patient details:")
                
                for consult in all_consultations:
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
                            st.write(f"**Created:** {selected_consult.get('created_at', 'N/A')}")
                        
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
                            with img_col2:
                                if selected_consult['patient'].get('xray_image'):
                                    st.markdown("**🩻 X-Ray Image:**")
                                    st.image(f"http://localhost:8000/uploads/{selected_consult['patient']['xray_image']}", 
                                           caption="X-Ray", width=400)
                        
                        # Cardiologist Response
                        if selected_consult['status'] in ['reviewed', 'completed']:
                            st.markdown("---")
                            st.markdown("**Cardiologist Response:**")
                            st.write(f"Cardiologist: {selected_consult.get('cardiologist_name', 'N/A')}")
                            st.write(f"Email: {selected_consult.get('cardiologist_email', 'N/A')}")
                            st.write(f"**Diagnosis:** {selected_consult.get('diagnosis', 'N/A')}")
                            st.write(f"**Recommendations:** {selected_consult.get('recommendations', 'N/A')}")
                            st.write(f"**Notes:** {selected_consult.get('cardiologist_notes', 'N/A')}")
                            st.write(f"**Response Date:** {selected_consult.get('response_date', 'N/A')}")
                        
                        if st.button("❌ Close Patient File"):
                            del st.session_state.selected_patient
                            st.rerun()
            else:
                st.info("No patient records found")
        except Exception as e:
            st.warning(f"⚠️ Could not load patient references: {e}")
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
