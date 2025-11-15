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
1. Navigate to **"Register New Doctor"** page
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

### ✅ Test 2: GP Clinician Registration
**Objective**: Register a GP Clinician without NSR requirement

**Test Data**:
```
Full Name: Dr. Ahmad bin Ali
Email: ahmad@clinic.com
Role: GP Clinician
Hospital/Clinic: Klinik Kesihatan Bandar
IC/Passport: 900101-01-1234
MMC No.: MMC12345
NSR No.: (should not appear)
```

**Steps**:
1. Fill all fields with test data above
2. Verify NSR field is hidden
3. Click **Register** button
4. **Expected**: Success message "✅ Doctor registered successfully!"
5. Verify JSON response shows doctor details

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 3: Cardiologist Registration with NSR
**Objective**: Register a Cardiologist with mandatory NSR validation

**Test Data**:
```
Full Name: Dr. Sarah Lim
Email: sarah@hospital.com
Role: Cardiologist
Hospital/Clinic: Hospital Jantung Negara
IC/Passport: 850505-05-5678
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

### ✅ Test 4: Create New Consultation
**Objective**: GP creates consultation with patient details and medical images

**Test Data**:
```
GP Email: ahmad@clinic.com

Patient Information:
- Name: Ahmad Ismail
- IC Number: 700808-01-5678
- Age: 55
- Gender: Male
- Symptoms: Chest pain radiating to left arm, shortness of breath

Vital Signs:
- Blood Pressure: 150/95
- Heart Rate: 95 bpm
- Temperature: 37.2°C
- SpO2: 96%
- Respiratory Rate: 20
```

**Steps**:
1. Navigate to **"New Consultation"** page
2. Fill GP email and patient information
3. Enter symptoms in text area
4. Fill all vital signs
5. Upload ECG image (any .jpg, .png, or .pdf file)
6. Upload X-Ray image (any .jpg, .png, or .pdf file)
7. Click **Submit Consultation**
8. **Expected**: Success message, consultation ID generated

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 5: View Consultation Details
**Objective**: Verify all consultation data displays correctly

**Steps**:
1. Navigate to **"View Consultations"** page
2. Select the consultation created in Test 4
3. Verify the following sections display correctly:

**GP Clinician Information**:
   - ☐ Name: Dr. Ahmad bin Ali
   - ☐ Hospital: Klinik Kesihatan Bandar
   - ☐ MMC No.: MMC12345

**Patient Information**:
   - ☐ Name: Ahmad Ismail
   - ☐ IC: 700808-01-5678
   - ☐ Age: 55
   - ☐ Gender: Male

**Clinical Information**:
   - ☐ Symptoms displayed correctly
   - ☐ All vital signs visible (BP, HR, Temp, SpO2, RR)

**Medical Images**:
   - ☐ ECG image displays
   - ☐ X-Ray image displays

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 6: Generate Referral Letter PDF
**Objective**: Create and download professional referral letter

**Test Data**:
```
Reason for Referral:
"Patient presenting with acute chest pain and dyspnea. 
ECG shows ST elevation in leads II, III, aVF. 
Require urgent cardiology review for possible acute coronary syndrome.
Troponin levels elevated at 2.5 ng/mL."
```

**Steps**:
1. In **"View Consultations"**, select the consultation
2. Scroll to **"Generate Referral Letter"** section
3. Enter the referral reason in text area
4. Click **"Generate Referral Letter"** button
5. Wait for success message
6. Click **"Download Referral Letter PDF"** button
7. Open downloaded PDF file

**PDF Content Verification**:
   - ☐ Header shows "REFERRAL LETTER TO CARDIOLOGIST"
   - ☐ "GPLink Cardio™" branding visible
   - ☐ Current date displayed
   - ☐ GP details section (name, hospital, MMC, email)
   - ☐ Patient information table complete
   - ☐ Vital signs table with all values
   - ☐ Referral reason text appears
   - ☐ Professional formatting (margins, spacing)
   - ☐ Footer shows "DRAHMADSYAHID © 2025"
   - ☐ No layout issues or text overflow

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 7: Cardiologist Response
**Objective**: Cardiologist reviews and responds to consultation

**Test Data**:
```
Cardiologist Email: sarah@hospital.com
Diagnosis: Acute STEMI - ST Elevation Myocardial Infarction
Recommendations: Immediate admission to CCU, cardiac catheterization within 90 minutes, dual antiplatelet therapy (Aspirin 300mg + Clopidogrel 600mg), IV heparin, morphine for pain control
Notes: Patient requires urgent PCI. Advise immediate transfer to cardiac catheterization lab. High risk for cardiogenic shock. Monitor vitals closely.
```

**Steps**:
1. Navigate to **"Respond to Consultation"** page
2. Select the consultation from dropdown
3. Enter cardiologist email
4. Fill diagnosis field
5. Fill recommendations field
6. Fill cardiologist notes
7. Click **Submit Response**
8. **Expected**: Success message, response saved

**Verification**:
9. Go back to **"View Consultations"**
10. Select same consultation
11. Verify response appears in consultation details

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 8: Statistics Dashboard
**Objective**: Verify system statistics display correctly

**Steps**:
1. Navigate to **"Statistics"** page
2. Verify the following metrics:

**Expected Values** (based on tests above):
   - ☐ Total Consultations: 1 or more
   - ☐ Pending consultations count
   - ☐ Reviewed consultations count
   - ☐ Completed consultations count
   - ☐ Metrics display with colored indicators

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 9: Branding & UI Consistency
**Objective**: Verify GPLink Cardio™ branding throughout application

**Checklist** (verify on ALL pages):
   - ☐ Page title: "GPLink Cardio™"
   - ☐ Subtitle: "GP-Cardiologist Consultation Portal"
   - ☐ All references say "GP Clinician" (not "Clinic Doctor")
   - ☐ Theme color #9A7D61 (brown/tan) visible in headers
   - ☐ Copyright footer "DRAHMADSYAHID © 2025" on Home page
   - ☐ Navigation menu shows all 6 pages
   - ☐ No spelling errors in labels
   - ☐ Professional appearance throughout

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

### ✅ Test 10: Error Handling
**Objective**: Verify appropriate error messages

**Test Cases**:

**A. Empty Form Submission**:
1. Go to "Register New Doctor"
2. Leave all fields empty
3. Click Register
4. **Expected**: Warning message about required fields

**B. Invalid Email Format**:
1. Enter invalid email (e.g., "notanemail")
2. Try to register
3. **Expected**: Email validation error

**C. Missing Backend Connection**:
1. Stop backend server
2. Try to register or create consultation
3. **Expected**: Error message or connection warning
4. Restart backend and verify recovery

**Status**: ☐ Pass ☐ Fail  
**Notes**: _______________________________

---

## 📊 Test Summary

| Test # | Test Name | Status | Priority |
|--------|-----------|--------|----------|
| 1 | Dynamic NSR Field | ☐ | Critical |
| 2 | GP Registration | ☐ | High |
| 3 | Cardiologist Registration | ☐ | High |
| 4 | Create Consultation | ☐ | High |
| 5 | View Consultation | ☐ | High |
| 6 | Generate PDF | ☐ | Critical |
| 7 | Cardiologist Response | ☐ | Medium |
| 8 | Statistics | ☐ | Low |
| 9 | Branding | ☐ | Medium |
| 10 | Error Handling | ☐ | High |

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
