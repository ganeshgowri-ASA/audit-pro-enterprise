"""
Configuration settings for Audit Pro Enterprise
"""
import os
from pathlib import Path
from typing import Optional

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/audit_pro.db")

# Application settings
APP_NAME = "Audit Pro Enterprise"
APP_VERSION = "1.0.0"

# Entity hierarchy levels
ENTITY_TYPES = {
    0: "Corporate",
    1: "Plant",
    2: "Line",
    3: "Process",
    4: "Sub-Process"
}

MAX_HIERARCHY_LEVEL = 4

# Streamlit configuration
STREAMLIT_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": "🏢",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}
