"""Configuration settings for the Streamlit frontend."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "1200"))  # Increased from 500 to 1200 seconds (20 minutes)

# Streamlit configuration
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
