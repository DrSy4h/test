"""
Generate Testing Guide PDF for GPLink Cardio
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

# Create PDF
pdf = SimpleDocTemplate(
    "GPLink_Cardio_Testing_Guide.pdf",
    pagesize=A4,
    rightMargin=50,
    leftMargin=50,
    topMargin=50,
    bottomMargin=30
)

elements = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#9A7D61'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#9A7D61'),
    spaceAfter=12,
    spaceBefore=20,
    fontName='Helvetica-Bold'
)

subheading_style = ParagraphStyle(
    'CustomSubHeading',
    parent=styles['Heading3'],
    fontSize=12,
    textColor=colors.HexColor('#9A7D61'),
    spaceAfter=8,
    spaceBefore=15,
    fontName='Helvetica-Bold'
)

normal = styles['Normal']
normal.fontSize = 10
normal.leading = 14

# Title Page
elements.append(Paragraph("GPLink Cardio™", title_style))
elements.append(Paragraph("TESTING GUIDE", ParagraphStyle('subtitle', parent=title_style, fontSize=18)))
elements.append(Spacer(1, 0.5*inch))

# System Information
elements.append(Paragraph("System Information", heading_style))
info_data = [
    ['Application:', 'GPLink Cardio™ - GP-Cardiologist Consultation Portal'],
    ['Version:', '1.0'],
    ['Developer:', 'DRAHMADSYAHID © 2025'],
    ['Testing Date:', f'November {datetime.now().year}'],
    ['Backend URL:', 'http://127.0.0.1:8000'],
    ['Frontend URL:', 'http://localhost:8501'],
    ['Database:', 'MongoDB - gplink_db']
]
info_table = Table(info_data, colWidths=[2*inch, 4.5*inch])
info_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#9A7D61')),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
]))
elements.append(info_table)
elements.append(PageBreak())

# Test 1
elements.append(Paragraph("Test 1: Dynamic NSR Field ✅ (Critical)", heading_style))
elements.append(Paragraph("<b>Objective:</b> Verify NSR field appears dynamically based on role selection", normal))
elements.append(Spacer(1, 0.1*inch))
elements.append(Paragraph("<b>Steps:</b>", normal))
test1_steps = """
1. Navigate to "Register New Doctor" page<br/>
2. Observe the Role dropdown<br/>
3. Select "GP Clinician" from dropdown → Expected: NSR field is NOT visible<br/>
4. Select "Cardiologist" from dropdown → Expected: NSR field appears instantly<br/>
5. Toggle between roles multiple times → Expected: Field shows/hides smoothly
"""
elements.append(Paragraph(test1_steps, normal))
elements.append(Paragraph("<b>Status:</b> ☐ Pass  ☐ Fail  |  <b>Notes:</b> _________________", normal))
elements.append(Spacer(1, 0.2*inch))

# Test 2
elements.append(Paragraph("Test 2: GP Clinician Registration ✅", heading_style))
elements.append(Paragraph("<b>Objective:</b> Register a GP Clinician without NSR requirement", normal))
elements.append(Spacer(1, 0.1*inch))
test2_data = [
    ['Field', 'Test Data'],
    ['Full Name', 'Dr. Ahmad bin Ali'],
    ['Email', 'ahmad@clinic.com'],
    ['Role', 'GP Clinician'],
    ['Hospital/Clinic', 'Klinik Kesihatan Bandar'],
    ['IC/Passport', '900101-01-1234'],
    ['MMC No.', 'MMC12345'],
    ['NSR No.', '(should not appear)']
]
test2_table = Table(test2_data, colWidths=[2*inch, 4.5*inch])
test2_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9A7D61')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
]))
elements.append(test2_table)
elements.append(Paragraph("<b>Expected:</b> Success message '✅ Doctor registered successfully!'", normal))
elements.append(Paragraph("<b>Status:</b> ☐ Pass  ☐ Fail  |  <b>Notes:</b> _________________", normal))
elements.append(Spacer(1, 0.2*inch))

# Test 3
elements.append(Paragraph("Test 3: Cardiologist Registration with NSR ✅", heading_style))
elements.append(Paragraph("<b>Objective:</b> Register Cardiologist with mandatory NSR validation", normal))
elements.append(Spacer(1, 0.1*inch))
test3_data = [
    ['Field', 'Test Data'],
    ['Full Name', 'Dr. Sarah Lim'],
    ['Email', 'sarah@hospital.com'],
    ['Role', 'Cardiologist'],
    ['Hospital/Clinic', 'Hospital Jantung Negara'],
    ['IC/Passport', '850505-05-5678'],
    ['MMC No.', 'MMC67890'],
    ['NSR No.', 'NSR2024001 (REQUIRED)']
]
test3_table = Table(test3_data, colWidths=[2*inch, 4.5*inch])
test3_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9A7D61')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
]))
elements.append(test3_table)
elements.append(Paragraph("<b>Validation:</b> Try registering WITHOUT NSR → Should show error", normal))
elements.append(Paragraph("<b>Status:</b> ☐ Pass  ☐ Fail  |  <b>Notes:</b> _________________", normal))
elements.append(PageBreak())

# Test 4
elements.append(Paragraph("Test 4: Create New Consultation ✅", heading_style))
elements.append(Paragraph("<b>Objective:</b> GP creates consultation with patient details and medical images", normal))
elements.append(Spacer(1, 0.1*inch))
test4_data = [
    ['Category', 'Details'],
    ['GP Email', 'ahmad@clinic.com'],
    ['Patient Name', 'Ahmad Ismail'],
    ['IC Number', '700808-01-5678'],
    ['Age', '55'],
    ['Gender', 'Male'],
    ['Symptoms', 'Chest pain radiating to left arm, shortness of breath'],
    ['Blood Pressure', '150/95'],
    ['Heart Rate', '95 bpm'],
    ['Temperature', '37.2°C'],
    ['SpO2', '96%'],
    ['Respiratory Rate', '20'],
    ['ECG Image', 'Upload any .jpg/.png/.pdf'],
    ['X-Ray Image', 'Upload any .jpg/.png/.pdf']
]
test4_table = Table(test4_data, colWidths=[2*inch, 4.5*inch])
test4_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#9A7D61')),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
]))
elements.append(test4_table)
elements.append(Paragraph("<b>Expected:</b> Success message, consultation ID generated", normal))
elements.append(Paragraph("<b>Status:</b> ☐ Pass  ☐ Fail  |  <b>Notes:</b> _________________", normal))
elements.append(Spacer(1, 0.2*inch))

# Test 5
elements.append(Paragraph("Test 5: View Consultation Details ✅", heading_style))
elements.append(Paragraph("<b>Objective:</b> Verify all consultation data displays correctly", normal))
elements.append(Spacer(1, 0.1*inch))
checklist = """
<b>Verification Checklist:</b><br/>
☐ GP Clinician Info: Name, Hospital, MMC No.<br/>
☐ Patient Info: Name, IC, Age, Gender<br/>
☐ Clinical Info: Symptoms, all vital signs<br/>
☐ Medical Images: ECG and X-Ray images display<br/>
"""
elements.append(Paragraph(checklist, normal))
elements.append(Paragraph("<b>Status:</b> ☐ Pass  ☐ Fail  |  <b>Notes:</b> _________________", normal))
elements.append(Spacer(1, 0.2*inch))

# Test 6
elements.append(Paragraph("Test 6: Generate Referral Letter PDF ✅ (Critical)", heading_style))
elements.append(Paragraph("<b>Objective:</b> Create and download professional referral letter", normal))
elements.append(Spacer(1, 0.1*inch))
elements.append(Paragraph("<b>Referral Reason Example:</b>", normal))
reason_text = """
"Patient presenting with acute chest pain and dyspnea. ECG shows ST elevation 
in leads II, III, aVF. Require urgent cardiology review for possible acute 
coronary syndrome. Troponin levels elevated at 2.5 ng/mL."
"""
elements.append(Paragraph(reason_text, ParagraphStyle('italic', parent=normal, fontName='Helvetica-Oblique')))
elements.append(Spacer(1, 0.1*inch))
elements.append(Paragraph("<b>PDF Content Verification:</b>", normal))
pdf_checks = """
☐ Header: "REFERRAL LETTER TO CARDIOLOGIST"<br/>
☐ GPLink Cardio™ branding visible<br/>
☐ Current date displayed<br/>
☐ GP details (name, hospital, MMC, email)<br/>
☐ Patient information table<br/>
☐ Vital signs table<br/>
☐ Referral reason text<br/>
☐ Professional formatting<br/>
☐ Footer: "DRAHMADSYAHID © 2025"<br/>
☐ No layout issues
"""
elements.append(Paragraph(pdf_checks, normal))
elements.append(Paragraph("<b>Status:</b> ☐ Pass  ☐ Fail  |  <b>Notes:</b> _________________", normal))
elements.append(PageBreak())

# Test 7
elements.append(Paragraph("Test 7: Cardiologist Response ✅", heading_style))
test7_data = [
    ['Field', 'Test Data'],
    ['Cardiologist Email', 'sarah@hospital.com'],
    ['Diagnosis', 'Acute STEMI - ST Elevation Myocardial Infarction'],
    ['Recommendations', 'Immediate admission to CCU, cardiac catheterization within 90 minutes, dual antiplatelet therapy'],
    ['Notes', 'Patient requires urgent PCI. Advise immediate transfer to cardiac cath lab. High risk.']
]
test7_table = Table(test7_data, colWidths=[2*inch, 4.5*inch])
test7_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#9A7D61')),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP')
]))
elements.append(test7_table)
elements.append(Paragraph("<b>Verification:</b> Go to View Consultations and verify response appears", normal))
elements.append(Paragraph("<b>Status:</b> ☐ Pass  ☐ Fail  |  <b>Notes:</b> _________________", normal))
elements.append(Spacer(1, 0.2*inch))

# Test 8
elements.append(Paragraph("Test 8: Statistics Dashboard ✅", heading_style))
stats_checks = """
<b>Verify Metrics Display:</b><br/>
☐ Total Consultations count<br/>
☐ Pending consultations<br/>
☐ Reviewed consultations<br/>
☐ Completed consultations<br/>
☐ Color indicators visible
"""
elements.append(Paragraph(stats_checks, normal))
elements.append(Paragraph("<b>Status:</b> ☐ Pass  ☐ Fail  |  <b>Notes:</b> _________________", normal))
elements.append(Spacer(1, 0.2*inch))

# Test 9
elements.append(Paragraph("Test 9: Branding & UI Consistency ✅", heading_style))
brand_checks = """
<b>Verify on ALL pages:</b><br/>
☐ Page title: "GPLink Cardio™"<br/>
☐ Subtitle: "GP-Cardiologist Consultation Portal"<br/>
☐ All references say "GP Clinician" (not "Clinic Doctor")<br/>
☐ Theme color #9A7D61 visible in headers<br/>
☐ Copyright footer "DRAHMADSYAHID © 2025" on Home<br/>
☐ Navigation menu shows all 6 pages<br/>
☐ Professional appearance
"""
elements.append(Paragraph(brand_checks, normal))
elements.append(Paragraph("<b>Status:</b> ☐ Pass  ☐ Fail  |  <b>Notes:</b> _________________", normal))
elements.append(Spacer(1, 0.2*inch))

# Test 10
elements.append(Paragraph("Test 10: Error Handling ✅", heading_style))
error_tests = """
<b>A. Empty Form Submission:</b> Leave all fields empty → Should show warning<br/>
<b>B. Invalid Email:</b> Enter "notanemail" → Should show validation error<br/>
<b>C. Backend Connection:</b> Stop backend → Should show connection error
"""
elements.append(Paragraph(error_tests, normal))
elements.append(Paragraph("<b>Status:</b> ☐ Pass  ☐ Fail  |  <b>Notes:</b> _________________", normal))
elements.append(PageBreak())

# Summary Table
elements.append(Paragraph("Test Summary", heading_style))
summary_data = [
    ['#', 'Test Name', 'Priority', 'Status'],
    ['1', 'Dynamic NSR Field', 'Critical', '☐'],
    ['2', 'GP Registration', 'High', '☐'],
    ['3', 'Cardiologist Registration', 'High', '☐'],
    ['4', 'Create Consultation', 'High', '☐'],
    ['5', 'View Consultation', 'High', '☐'],
    ['6', 'Generate PDF', 'Critical', '☐'],
    ['7', 'Cardiologist Response', 'Medium', '☐'],
    ['8', 'Statistics', 'Low', '☐'],
    ['9', 'Branding', 'Medium', '☐'],
    ['10', 'Error Handling', 'High', '☐']
]
summary_table = Table(summary_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1*inch])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9A7D61')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
]))
elements.append(summary_table)
elements.append(Spacer(1, 0.3*inch))

# Sign-off
elements.append(Paragraph("Sign-Off", heading_style))
signoff = """
<b>Tester Name:</b> _________________________________<br/>
<b>Date Tested:</b> _________________________________<br/>
<b>Overall Result:</b> ☐ All Tests Passed  ☐ Issues Found<br/>
<b>Recommendation:</b> ☐ Ready for Production  ☐ Requires Fixes<br/>
<br/>
<b>Additional Comments:</b><br/>
_________________________________________________________<br/>
_________________________________________________________<br/>
_________________________________________________________
"""
elements.append(Paragraph(signoff, normal))
elements.append(Spacer(1, 0.5*inch))

# Footer
footer_style = ParagraphStyle('footer', parent=normal, fontSize=10, textColor=colors.HexColor('#9A7D61'), alignment=TA_CENTER)
elements.append(Paragraph("<b>GPLink Cardio™ | DRAHMADSYAHID © 2025</b>", footer_style))

# Build PDF
pdf.build(elements)
print("✅ Testing Guide PDF generated: GPLink_Cardio_Testing_Guide.pdf")
