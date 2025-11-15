"""
GPLink - Streamlit Frontend
User interface for clinic doctors and cardiologists
"""

import streamlit as st
import requests
import json
from datetime import datetime

# API Base URL
API_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="GPLink - Doctor Consultation System",
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

def register_doctor(name, email, role, hospital_clinic):
    """Register a new doctor"""
    payload = {
        "name": name,
        "email": email,
        "role": role,
        "hospital_clinic": hospital_clinic
    }
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

# ============= MAIN APP =============

# Custom header with theme color
st.markdown("""
<div class="main-header">
    <h1>GPLink - Doctor Consultation System</h1>
    <p>Connecting clinic doctors with cardiologists for better patient care</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation with custom styling
st.sidebar.markdown("### 📋 Navigation Menu")
page = st.sidebar.selectbox(
    "Select Page",
    ["🏠 Home", "👨‍⚕️ Register Doctor", "➕ New Consultation", "📋 View Consultations", "💬 Respond to Consultation", "📊 Statistics"]
)

# ============= HOME PAGE =============

if page == "🏠 Home":
    st.header("Welcome to GPLink!")
    st.markdown("""
    ### About GPLink
    GPLink is a consultation system that connects clinic doctors with specialist cardiologists.
    
    **For Clinic Doctors:**
    - Submit consultation requests for patients with cardiac concerns
    - Get expert advice from cardiologists
    - Track consultation status
    
    **For Cardiologists:**
    - Review consultation requests from clinic doctors
    - Provide diagnosis and recommendations
    - Help improve patient outcomes
    
    **Getting Started:**
    1. Register as a doctor (Clinic Doctor or Cardiologist)
    2. Clinic doctors can create new consultations
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

elif page == "👨‍⚕️ Register Doctor":
    st.header("Register New Doctor")
    
    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        role = st.selectbox("Role", ["clinic_doctor", "cardiologist"])
        hospital_clinic = st.text_input("Hospital/Clinic Name")
        
        submit = st.form_submit_button("Register")
        
        if submit:
            if name and email and hospital_clinic:
                try:
                    result = register_doctor(name, email, role, hospital_clinic)
                    st.success(f"✅ Doctor registered successfully!")
                    st.json(result)
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("Please fill in all fields")

# ============= NEW CONSULTATION =============

elif page == "➕ New Consultation":
    st.header("Create New Consultation Request")
    
    with st.form("consultation_form"):
        st.subheader("Clinic Doctor Information")
        clinic_doctor_email = st.text_input("Your Email (Clinic Doctor)")
        
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
