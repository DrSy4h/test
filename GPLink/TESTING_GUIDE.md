# GPLink Cardio™ Testing Guide

## System Information
- **Application**: GPLink Cardio™ - GP-Cardiologist Consultation Portal
- **Version**: 1.0
- **Developer**: DRAHMADSYAHID © 2025
- **Testing Date**: November 2025

---

## Prerequisites
- Backend running on: http://127.0.0.1:8000
- Frontend running on: http://localhost:8501
- MongoDB connected to: gplink_db

---

## 📋 TESTING CHECKLIST

### ✅ Test 1: Dynamic NSR Field (Critical Feature)
**Objective**: Verify NSR field appears dynamically based on role selection

**Steps**:
1. Navigate to **"👨‍⚕️ Register New Doctor"** page
2. Observe the Role dropdown
3. Select **"GP Clinician"** from dropdown
   - **Expected**: NSR field is NOT visible
4. Select **"Cardiologist"** from dropdown
   - **Expected**: NSR field appears instantly with label "NSR No. * (Compulsory for Cardiologists)"
5. Toggle between roles multiple times
   - **Expected**: Field shows/hides smoothly without errors

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 2: Real-time Email Validation
**Objective**: Verify instant email validation before form submission

**Steps**:
1. Navigate to **"➕ New Consultation"** page
2. In "GP Email" field, type an unregistered email (e.g., "test@test.com")
3. Press Enter or Tab to trigger validation
   - **Expected**: Red warning "⚠️ GP not found in database. Please register first."
4. Enter a registered GP email (e.g., "ahmad@clinic.com")
   - **Expected**: Green success message "✅ GP found: Dr. Ahmad bin Ali (Klinik Kesihatan Bandar)"

**Cardiologist Validation Test**:
5. Navigate to **"💬 Respond to Consultation"** page
6. Enter unregistered email in Cardiologist field
   - **Expected**: Red warning "⚠️ Cardiologist not found in database. Please register first."
7. Enter registered cardiologist email
   - **Expected**: Green success "✅ Cardiologist found: [name] ([hospital])"

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 3: GP Clinician Registration
**Objective**: Register a GP Clinician without NSR requirement

**Test Data**:
```
Full Name: Dr. Ahmad bin Ali
Email: ahmad@clinic.com
Role: GP Clinician
Hospital/Clinic: Klinik Kesihatan Bandar
IC/Passport No: 900101-01-1234
MMC No.: MMC12345
NSR No.: (should not appear)
```

**Steps**:
1. Navigate to **"👨‍⚕️ Register New Doctor"** page
2. Fill all fields with test data above
3. Verify NSR field is hidden
4. Click **Register** button
5. **Expected**: Success message "✅ Doctor registered successfully!"
6. Verify JSON response shows doctor details

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 4: Cardiologist Registration with NSR
**Objective**: Register a Cardiologist with mandatory NSR validation

**Test Data**:
```
Full Name: Dr. Sarah Lim
Email: sarah@hospital.com
Role: Cardiologist
Hospital/Clinic: Hospital Jantung Negara
IC/Passport No: 850505-05-5678
MMC No.: MMC67890
NSR No.: NSR2024001
```

**Steps**:
1. Fill all fields with test data above
2. Verify NSR field is visible and marked with *
3. Click **Register** button
4. **Expected**: Success message with doctor details

**Validation Test**:
5. Try registering Cardiologist WITHOUT filling NSR
6. **Expected**: Error message "❌ NSR No. is compulsory for Cardiologists!"

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 5: Create New Consultation
**Objective**: GP creates consultation with patient details and medical images

**Test Data**:
```
GP Email: ahmad@clinic.com

Patient Information:
- Name: Ahmad Ismail
- IC/Passport No: 700808-01-5678
- Age: 55
- Gender: Male
- Symptoms: Chest pain radiating to left arm, shortness of breath

Vital Signs:
- Blood Pressure: 150/95
- Heart Rate: 95 bpm
- Temperature: 37.2°C
- SpO2: 96%
- Respiratory Rate: 20

Urgency: 🔴 Emergency
```

**Steps**:
1. Navigate to **"➕ New Consultation"** page
2. Enter GP email and wait for validation ✅
3. Fill patient information (note: field says "IC/Passport No")
4. Enter symptoms in text area
5. Fill all vital signs
6. Select urgency from dropdown (🟢 Normal / 🟡 Urgent / 🔴 Emergency)
7. Upload ECG image (optional - .jpg, .png, or .pdf)
8. Upload X-Ray image (optional - .jpg, .png, or .pdf)
9. Click **Submit Consultation**
10. **Expected**: Success message, consultation ID generated

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 6: Edit Consultation with Image Management
**Objective**: Edit pending consultation and manage medical images

**Steps**:
1. Navigate to **"📋 View Consultations"** page
2. Filter by "Pending" status
3. Find the consultation created in Test 5
4. Click **"📝 Edit"** button
5. **Expected**: Edit form appears with pre-filled data

**Image Removal Test**:
6. If ECG image exists, check "Remove ECG image" checkbox
7. Click **Update Consultation**
8. **Expected**: Success message, ECG image removed

**Image Upload Test**:
9. Click **"📝 Edit"** again
10. Use "Upload New ECG Image" uploader
11. Select a new image file
12. Click **Update Consultation**
13. **Expected**: New image uploaded and displayed

**Image Replace Test**:
14. Edit again, check "Remove X-Ray image" AND upload new X-Ray
15. Update consultation
16. **Expected**: Old image removed, new image displayed

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 7: Manage Doctors
**Objective**: Test doctor management with separate sections

**Steps**:
1. Navigate to **"👥 Manage Doctors"** page
2. Verify two sections:
   - **❤️ Cardiologists** (shows NSR numbers)
   - **🩺 GP Clinicians**

**Search Test**:
3. Enter "sarah" in search box
4. **Expected**: Filters to show only Dr. Sarah Lim

**Edit Doctor Test**:
5. Click **"✏️ Edit"** on any doctor
6. Change hospital name
7. Click **"Save Changes"**
8. **Expected**: Success message "✅ Doctor updated successfully!"

**Delete Doctor Test**:
9. Click **"🗑️ Delete"** on a test doctor
10. **Expected**: Confirmation dialog appears
11. Click **"Yes, Delete"**
12. **Expected**: Success message, doctor removed from list

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 8: View Consultation Details
**Objective**: Verify all consultation data displays correctly

**Steps**:
1. Navigate to **"📋 View Consultations"** page
2. Select the consultation created in Test 5
3. Verify the following sections display correctly:

**GP Clinician Information**:
   - ☐ Name: Dr. Ahmad bin Ali
   - ☐ Hospital: Klinik Kesihatan Bandar
   - ☐ MMC No.: MMC12345
   - ☐ Display says "GP Clinician" (not "clinic_doctor")

**Patient Information**:
   - ☐ Name: Ahmad Ismail
   - ☐ IC/Passport No: 700808-01-5678 (field labeled correctly)
   - ☐ Age: 55
   - ☐ Gender: Male

**Clinical Information**:
   - ☐ Symptoms displayed correctly
   - ☐ All vital signs visible (BP, HR, Temp, SpO2, RR)
   - ☐ Urgency shows with emoji indicator

**Medical Images**:
   - ☐ ECG image displays (if uploaded)
   - ☐ X-Ray image displays (if uploaded)

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 9: Cardiologist Response
**Objective**: Cardiologist reviews and responds to consultation

**Test Data**:
```
Cardiologist Email: sarah@hospital.com
Diagnosis: Acute STEMI - ST Elevation Myocardial Infarction
Recommendations: Immediate admission to CCU, cardiac catheterization within 90 minutes, dual antiplatelet therapy (Aspirin 300mg + Clopidogrel 600mg), IV heparin, morphine for pain control
Notes: Patient requires urgent PCI. Advise immediate transfer to cardiac catheterization lab. High risk for cardiogenic shock. Monitor vitals closely.
```

**Steps**:
1. Navigate to **"💬 Respond to Consultation"** page
2. Enter cardiologist email and wait for validation ✅
3. Select the pending consultation from dropdown
4. **Expected**: Consultation details displayed with patient info and images
5. Fill diagnosis field
6. Fill recommendations field
7. Fill cardiologist notes
8. Click **Submit Response**
9. **Expected**: Success message, status changed to "Reviewed"

**Verification**:
10. Go to **"📋 View Consultations"**
11. Filter by "Reviewed" status
12. Select same consultation
13. Verify cardiologist response appears with all fields

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 10: GP Decision Workflow (Complete Consultation)
**Objective**: Test GP decision buttons for reviewed consultations

**Steps**:
1. Navigate to **"📋 View Consultations"** page
2. Filter by "Reviewed" status
3. Select consultation with cardiologist response
4. **Expected**: Two buttons visible:
   - ✅ **Complete Consultation**
   - 💬 **Continue Discussion**

**Complete Consultation Test**:
5. Click **"✅ Complete Consultation"**
6. **Expected**: Warning dialog appears:
   - "⚠️ Confirm Completion"
   - "Are you sure you want to mark this consultation as completed?"
   - Buttons: "Yes, Complete" and "No, Cancel"
7. Click **"Yes, Complete"**
8. **Expected**: Success message "✅ Consultation marked as completed!"
9. Refresh consultations list
10. Filter by "Completed" status
11. **Expected**: Consultation now appears in completed list

**Continue Discussion Test** (Placeholder):
12. For another reviewed consultation, click **"💬 Continue Discussion"**
13. **Expected**: Info message "(Feature coming soon)" or discussion interface

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 11: Generate Referral Letter PDF
**Objective**: Create and download professional referral letter with/without images

**Test Data**:
```
Reason for Referral:
"Patient presenting with acute chest pain and dyspnea. 
ECG shows ST elevation in leads II, III, aVF. 
Require urgent cardiology review for possible acute coronary syndrome.
Troponin levels elevated at 2.5 ng/mL."
```

**Steps**:
1. In **"📋 View Consultations"**, select a consultation
2. Scroll to **"Generate Referral Letter"** section
3. Enter the referral reason in text area
4. Check **"Include ECG Image"** (if available)
5. Check **"Include X-Ray Image"** (if available)
6. Click **"Generate Referral Letter"** button
7. Wait for success message
8. Click **"Download Referral Letter PDF"** button
9. Open downloaded PDF file

**PDF Content Verification**:
   - ☐ Header shows "REFERRAL LETTER TO CARDIOLOGIST"
   - ☐ "GPLink Cardio™" branding visible
   - ☐ Current date displayed
   - ☐ GP details section (name, hospital, MMC, email)
   - ☐ Patient information table with "IC/Passport No" label
   - ☐ Vital signs table with all values
   - ☐ Referral reason text appears
   - ☐ Medical images included (if selected)
   - ☐ Professional formatting (margins, spacing)
   - ☐ Footer shows "DRAHMADSYAHID © 2025"
   - ☐ No layout issues or text overflow

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 12: Statistics Dashboard with Patient Files
**Objective**: Verify statistics page with donut chart and patient file viewer

**Steps**:
1. Navigate to **"📊 Statistics"** page

**Metrics Verification**:
   - ☐ Total Consultations count
   - ☐ Total Doctors count
   - ☐ Pending consultations count
   - ☐ Reviewed consultations count
   - ☐ Completed consultations count

**Donut Chart Test**:
2. Verify donut chart displays:
   - ☐ Chart renders properly
   - ☐ Three segments: Pending (red), Reviewed (yellow), Completed (green)
   - ☐ Hover shows percentages
   - ☐ Legend displays correctly

**Statistics Table Test**:
3. Verify data table shows:
   - ☐ Variable column (Pending/Reviewed/Completed)
   - ☐ Count column with numbers
   - ☐ Percentage column with % values

**Patient File References Test**:
4. Scroll to **"📁 Patient File References"** section
5. Verify table columns:
   - ☐ Consultation ID (clickable 📁 icons)
   - ☐ Patient Name
   - ☐ GP Clinician
   - ☐ Status

**Patient File Viewer Test**:
6. Click any 📁 Consultation ID
7. **Expected**: Patient file modal/section opens showing:
   - ☐ Patient Information (Name, IC/Passport No, Age, Gender)
   - ☐ Clinical Data (Symptoms, Vital Signs, Urgency with emoji)
   - ☐ Medical Images (ECG/X-Ray if available)
   - ☐ GP Information
   - ☐ Cardiologist Response (if status = Reviewed/Completed)
   - ☐ Close button to return to list
8. Click **Close** button
9. **Expected**: Returns to patient file references table

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 13: Branding & UI Consistency
**Objective**: Verify GPLink Cardio™ branding and KPJ styling throughout application

**Sidebar Verification**:
   - ☐ KPJ Healthcare logo displays (250px width)
   - ☐ Logo positioned above navigation menu
   - ☐ Logo loads without errors

**Navigation Verification**:
   - ☐ Navigation uses radio buttons (not dropdown)
   - ☐ Radio buttons styled with brown background (#9A7D61)
   - ☐ Button text is white and readable
   - ☐ Hover effect: darker brown (#7D6550)
   - ☐ Selected state: darkest brown (#6B5640)
   - ☐ Text left-aligned with proper padding
   - ☐ All 7 pages listed: Home, Register, Manage Doctors, New Consultation, Respond, View, Statistics

**Content Checklist** (verify on ALL pages):
   - ☐ Page title: "GPLink Cardio™" or appropriate page heading
   - ☐ Subtitle: "GP-Cardiologist Consultation Portal" (Home page)
   - ☐ All references say "GP Clinician" (not "Clinic Doctor")
   - ☐ All forms use "IC/Passport No" (not just "IC Number")
   - ☐ Theme color #9A7D61 visible in navigation
   - ☐ Copyright footer "DRAHMADSYAHID © 2025" on Home page
   - ☐ No spelling errors in labels
   - ☐ Professional appearance throughout

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 14: Bulk Delete with Confirmation
**Objective**: Test multi-select delete functionality

**Steps**:
1. Navigate to **"📋 View Consultations"** page
2. Select checkboxes for 2-3 consultations
3. Click **"🗑️ Delete Selected"** button
4. **Expected**: Confirmation dialog:
   - "⚠️ Confirm Bulk Deletion"
   - "Are you sure you want to delete [X] consultations?"
   - Buttons: "Yes, Delete All" and "No, Cancel"
5. Click **"No, Cancel"**
6. **Expected**: Dialog closes, consultations NOT deleted

**Actual Deletion Test**:
7. Select consultations again
8. Click **"🗑️ Delete Selected"**
9. Click **"Yes, Delete All"**
10. **Expected**: Success message "✅ Successfully deleted [X] consultations"
11. Refresh list
12. **Expected**: Selected consultations removed

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 15: Error Handling
**Objective**: Verify appropriate error messages and recovery

**Test Cases**:

**A. Empty Form Submission**:
1. Go to "👨‍⚕️ Register New Doctor"
2. Leave all fields empty
3. Click Register
4. **Expected**: Warning message about required fields

**B. Invalid Email Format**:
1. Enter invalid email (e.g., "notanemail")
2. Try to create consultation
3. **Expected**: Real-time validation error (red warning)

**C. Unregistered Email**:
1. Try creating consultation with unregistered GP email
2. **Expected**: Red warning "⚠️ GP not found in database"

**D. Missing Backend Connection**:
1. Stop backend server
2. Try to register or create consultation
3. **Expected**: Error message or connection warning
4. Restart backend and verify recovery

**E. Edit Non-existent Consultation**:
1. Try to update consultation that was deleted
2. **Expected**: Error message "Consultation not found"

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

## 📊 Test Summary

| Test # | Test Name | Status | Priority |
|--------|-----------|--------|----------|
| 1 | Dynamic NSR Field | ☐ | Critical |
| 2 | Real-time Email Validation | ☐ | High |
| 3 | GP Registration | ☐ | High |
| 4 | Cardiologist Registration | ☐ | High |
| 5 | Create Consultation | ☐ | High |
| 6 | Edit Consultation & Images | ☐ | Critical |
| 7 | Manage Doctors | ☐ | High |
| 8 | View Consultation | ☐ | High |
| 9 | Cardiologist Response | ☐ | High |
| 10 | GP Decision Workflow | ☐ | Critical |
| 11 | Generate PDF | ☐ | Critical |
| 12 | Statistics & Patient Files | ☐ | Medium |
| 13 | Branding & UI | ☐ | Medium |
| 14 | Bulk Delete | ☐ | Medium |
| 15 | Error Handling | ☐ | High |

---

## 🐛 Bug Report Template

**Bug ID**: _______  
**Test #**: _______  
**Severity**: ☐ Critical ☐ High ☐ Medium ☐ Low  
**Description**: _________________________________  
**Steps to Reproduce**:
1. ___________________
2. ___________________
3. ___________________

**Expected Result**: _________________________________  
**Actual Result**: _________________________________  
**Screenshot**: _________________________________  
**Browser/Environment**: _________________________________

---

## ✅ Sign-Off

**Tester Name**: _______________________________  
**Date Tested**: _______________________________  
**Overall Result**: ☐ All Tests Passed ☐ Issues Found  
**Recommendation**: ☐ Ready for Production ☐ Requires Fixes  

**Additional Comments**:
_______________________________________________
_______________________________________________
_______________________________________________

---

**GPLink Cardio™ | DRAHMADSYAHID © 2025**
