import streamlit_app as st
import requests
import pandas as pd
from datetime import datetime
import json

# Configure the page
st.set_page_config(
    page_title="MongoDB Database Manager",
    page_icon=" =
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL (make sure your FastAPI server is running on this port)
API_BASE_URL = "http://localhost:8001"