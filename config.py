"""
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./audit_pro.db")

# Email Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "audit-system@example.com")

# Application Settings
APP_NAME = os.getenv("APP_NAME", "Audit Pro Enterprise")
APP_ENV = os.getenv("APP_ENV", "development")

# NC/OFI Settings
NC_OFI_TYPES = ["NC", "OFI"]
NC_CATEGORIES = ["Major", "Minor", "Observation"]
SEVERITY_LEVELS = ["Critical", "Major", "Minor"]
STATUS_WORKFLOW = ["Open", "InProgress", "Verified", "Closed"]
OVERDUE_THRESHOLD_DAYS = 7
