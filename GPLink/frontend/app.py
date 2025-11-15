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

def create_consultation(patient_data, symptoms, vital_signs, clinic_doctor_email, urgency):
    """Create new consultation"""
    payload = {
        "patient": patient_data,
        "symptoms": symptoms,
        "vital_signs": vital_signs,
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

def generate_referral_letter_pdf(consultation, gp_doctor, referral_reason=""):
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
        ['IC Number:', patient['ic_number']],
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
    elements.append(Spacer(1, 0.3*inch))
    
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

# Sidebar for navigation with custom styling
st.sidebar.markdown("### 📋 Navigation Menu")
page = st.sidebar.selectbox(
    "Select Page",
    ["🏠 Home", "👨‍⚕️ Register New Doctor", "➕ New Consultation", "📋 View Consultations", "💬 Respond to Consultation", "📊 Statistics"]
)

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

# ============= NEW CONSULTATION =============

elif page == "➕ New Consultation":
    st.header("Create New Consultation Request")
    
    with st.form("consultation_form"):
        st.subheader("GP Clinician Information")
        clinic_doctor_email = st.text_input("Your Email (GP Clinician)")
        
        st.subheader("Patient Information")
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.text_input("Patient Name")
            patient_age = st.number_input("Age", min_value=0, max_value=120)
        with col2:
            patient_gender = st.selectbox("Gender", ["Male", "Female"])
            patient_ic = st.text_input("IC Number")
        
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
        
        urgency = st.select_slider("Urgency", options=["normal", "urgent", "emergency"])
        
        submit = st.form_submit_button("Submit Consultation Request")
        
        if submit:
            if clinic_doctor_email and patient_name and symptoms:
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
                    
                    consultation_id = result['consultation_id']
                    st.success(f"✅ Consultation created successfully!")
                    st.info(f"Consultation ID: {consultation_id}")
                    
                    # Upload images if provided
                    if ecg_file:
                        try:
                            ecg_result = upload_ecg(consultation_id, ecg_file)
                            st.success(f"📎 ECG image uploaded: {ecg_result['filename']}")
                        except Exception as e:
                            st.warning(f"⚠️ ECG upload failed: {e}")
                    
                    if xray_file:
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
            for consult in consultations:
                with st.expander(f"🔍 {consult['consultation_id']} - {consult['patient']['name']} ({consult['status'].upper()})"):
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
                                   caption="ECG", use_container_width=True)
                        
                        if consult['patient'].get('xray_image'):
                            st.markdown("**🩻 X-Ray Image:**")
                            st.image(f"http://localhost:8000/uploads/{consult['patient']['xray_image']}", 
                                   caption="X-Ray", use_container_width=True)
                        
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
                    
                    # Generate Referral Letter button
                    st.markdown("---")
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        referral_reason = st.text_area(
                            "Reason for Referral (optional)",
                            value=f"Request for specialist cardiology opinion regarding {consult['symptoms'][:50]}...",
                            key=f"reason_{consult['consultation_id']}",
                            height=100
                        )
                    
                    with col2:
                        if st.button("📄 Generate Referral Letter", key=f"ref_{consult['consultation_id']}"):
                            try:
                                # Get GP doctor details
                                gp_email = consult['clinic_doctor_email']
                                gp_doctor_response = requests.get(f"{API_URL}/doctors/{gp_email}")
                                
                                if gp_doctor_response.status_code == 200:
                                    gp_doctor = gp_doctor_response.json()
                                    pdf_buffer = generate_referral_letter_pdf(consult, gp_doctor, referral_reason)
                                    
                                    st.download_button(
                                        label="💾 Download Referral Letter (PDF)",
                                        data=pdf_buffer,
                                        file_name=f"Referral_Letter_{consult['consultation_id']}_{consult['patient']['name'].replace(' ', '_')}.pdf",
                                        mime="application/pdf",
                                        key=f"download_{consult['consultation_id']}"
                                    )
                                    st.success("✅ Referral letter generated! Click Download button above.")
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
    
    cardiologist_email = st.text_input("Your Email (Cardiologist)")
    
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
                        if cardiologist_email and diagnosis and recommendations:
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
                                st.error(f"❌ Error: {e}")
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
        
        # Chart
        import pandas as pd
        chart_data = pd.DataFrame({
            'Status': ['Pending', 'Reviewed', 'Completed'],
            'Count': [stats["pending"], stats["reviewed"], stats["completed"]]
        })
        st.bar_chart(chart_data.set_index('Status'))
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
