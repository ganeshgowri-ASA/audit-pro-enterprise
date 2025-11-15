"""
Application Configuration Settings
AuditPro Enterprise
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/data/auditpro.db")

# Application settings
APP_NAME = "AuditPro Enterprise"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Enterprise Audit Management System - ISO 9001, IATF 16949, VDA 6.3"

# Session settings
SESSION_EXPIRY_HOURS = 24
SECRET_KEY = os.getenv("SECRET_KEY", "auditpro-enterprise-secret-key-change-in-production")

# File upload settings
UPLOAD_FOLDER = BASE_DIR / "data" / "uploads"
MAX_UPLOAD_SIZE_MB = 10
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'xlsx', 'docx'}

# Email settings (for notifications)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@auditpro.com")

# Audit settings
AUDIT_STATUSES = ["Planned", "In Progress", "Completed", "Cancelled"]
NC_SEVERITIES = ["Critical", "Major", "Minor", "Observation"]
NC_STATUSES = ["Open", "In Progress", "Closed", "Verified"]
CAR_STATUSES = ["Initiated", "Root Cause Analysis", "Action Plan", "Implementation", "Verification", "Closed"]

# Standards supported
STANDARDS = ["ISO 9001", "IATF 16949", "VDA 6.3", "AS9100", "ISO 14001", "ISO 45001"]

# User roles
USER_ROLES = ["Admin", "Auditor", "Quality Manager", "Department Head", "User"]

# Pagination
ITEMS_PER_PAGE = 20

# Chart colors
CHART_COLORS = {
    "primary": "#1f77b4",
    "success": "#2ca02c",
    "warning": "#ff7f0e",
    "danger": "#d62728",
    "info": "#17becf"
}

# Create necessary directories
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
(BASE_DIR / "data").mkdir(parents=True, exist_ok=True)
