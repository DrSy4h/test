"""
GPLink - AI Image Analysis Module
Uses Google Gemini API to analyze medical images (ECG, X-Ray)
"""

import os
import base64
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def analyze_ecg_image(image_path: str) -> str:
    """
    Analyze ECG image using Google Gemini API
    
    Args:
        image_path: Path to ECG image file
        
    Returns:
        AI analysis text describing the ECG findings
    """
    try:
        if not os.path.exists(image_path):
            return "Error: Image file not found"
        
        if not GEMINI_API_KEY:
            return "Error: Gemini API key not configured"
        
        # Read and encode image
        with open(image_path, "rb") as image_file:
            image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")
        
        # Determine image type
        file_ext = Path(image_path).suffix.lower()
        mime_type_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        mime_type = mime_type_map.get(file_ext, "image/jpeg")
        
        # Create Gemini model
        model = genai.GenerativeModel("gemini-pro-vision")
        
        # Prepare image for analysis
        image_part = {
            "mime_type": mime_type,
            "data": image_data
        }
        
        # Medical analysis prompt
        prompt = """Analyze this ECG (electrocardiogram) image and provide a medical assessment. 
        Include:
        1. Overall rhythm and rate assessment
        2. Any abnormalities detected
        3. QRS complex characteristics
        4. ST segment analysis
        5. Clinical significance and recommendations
        
        Please be concise but thorough, suitable for a cardiologist's review.
        Format the response in clear sections."""
        
        # Send to Gemini
        response = model.generate_content([prompt, image_part])
        
        return response.text
        
    except Exception as e:
        return f"Error analyzing ECG: {str(e)}"


def analyze_xray_image(image_path: str) -> str:
    """
    Analyze X-Ray image using Google Gemini API
    
    Args:
        image_path: Path to X-Ray image file
        
    Returns:
        AI analysis text describing the X-Ray findings
    """
    try:
        if not os.path.exists(image_path):
            return "Error: Image file not found"
        
        if not GEMINI_API_KEY:
            return "Error: Gemini API key not configured"
        
        # Read and encode image
        with open(image_path, "rb") as image_file:
            image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")
        
        # Determine image type
        file_ext = Path(image_path).suffix.lower()
        mime_type_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        mime_type = mime_type_map.get(file_ext, "image/jpeg")
        
        # Create Gemini model
        model = genai.GenerativeModel("gemini-pro-vision")
        
        # Prepare image for analysis
        image_part = {
            "mime_type": mime_type,
            "data": image_data
        }
        
        # Medical analysis prompt
        prompt = """Analyze this chest X-Ray image and provide a medical assessment.
        Include:
        1. Overall assessment of the chest cavity
        2. Heart size and shape evaluation
        3. Lung field analysis
        4. Any abnormalities or findings detected
        5. Clinical significance and recommendations
        
        Please be concise but thorough, suitable for a cardiologist's review.
        Format the response in clear sections."""
        
        # Send to Gemini
        response = model.generate_content([prompt, image_part])
        
        return response.text
        
    except Exception as e:
        return f"Error analyzing X-Ray: {str(e)}"


def analyze_medical_image(image_path: str, image_type: str) -> str:
    """
    Generic function to analyze medical images
    
    Args:
        image_path: Path to image file
        image_type: "ecg" or "xray"
        
    Returns:
        AI analysis text
    """
    if image_type.lower() == "ecg":
        return analyze_ecg_image(image_path)
    elif image_type.lower() == "xray":
        return analyze_xray_image(image_path)
    else:
        return "Error: Unknown image type. Use 'ecg' or 'xray'"
