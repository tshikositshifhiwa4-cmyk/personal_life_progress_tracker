"""
config.py — Environment & App Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()   # reads .env file if present

# ── DATABASE ──────────────────────────────────
DB_CONFIG = {
    'host':     os.environ.get('DB_HOST',     'localhost'),
    'port':     int(os.environ.get('DB_PORT', 5432)),
    'dbname':   os.environ.get('DB_NAME',     'personal_productivity'),
    'user':     os.environ.get('DB_USER',     'postgres'),
    'password': os.environ.get('DB_PASSWORD', ''),
}

# ── EMAIL ─────────────────────────────────────
EMAIL_CONFIG = {
    'sender':       os.environ.get('EMAIL_SENDER',   'your_email@gmail.com'),
    'recipient':    os.environ.get('EMAIL_RECIPIENT', 'your_email@gmail.com'),
    'app_password': os.environ.get('EMAIL_APP_PASSWORD', ''),
    'smtp_host':    'smtp.gmail.com',
    'smtp_port':    587,
}

# ── APP ───────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'princess-tracker-secret-change-in-prod')
DEBUG      = os.environ.get('DEBUG', 'True').lower() == 'true'
