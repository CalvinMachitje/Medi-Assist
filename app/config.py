import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  # load .env

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///medi_assist.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/static/uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    WTF_CSRF_ENABLED = os.environ.get('WTF_CSRF_ENABLED', 'True') == 'True'
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY', 'default_csrf_key')

    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Cache
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'SimpleCache')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))

    # Clinic Info
    CLINIC_NAME = os.environ.get('CLINIC_NAME')
    CLINIC_ADDRESS = os.environ.get('CLINIC_ADDRESS')
    CLINIC_PHONE = os.environ.get('CLINIC_PHONE')
    CLINIC_EMAIL = os.environ.get('CLINIC_EMAIL')

    EMERGENCY_SOUND_URL = os.environ.get('EMERGENCY_SOUND_URL')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # HTTPS only

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
