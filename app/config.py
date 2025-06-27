import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    YOLO_MODEL_PATH = os.getenv('YOLO_MODEL_PATH', 'models/best.pt')
    DEFAULT_RTSP_USERNAME = os.getenv('DEFAULT_RTSP_USERNAME', '')
    DEFAULT_RTSP_PASSWORD = os.getenv('DEFAULT_RTSP_PASSWORD', '')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',') if os.getenv('CORS_ORIGINS') else []