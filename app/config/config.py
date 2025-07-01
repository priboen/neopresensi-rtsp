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
    # DEEPFACE_MODEL = os.getenv('DEEPFACE_MODEL', 'Facenet512')
    DEEPFACE_MODEL = 'Facenet512'  # Default to Facenet512 if not set in .env
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
    CROPS_OUTPUT_DIR = os.getenv('CROPS_OUTPUT_DIR', 'crops')
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_DATABASE = os.getenv('DB_DATABASE', 'flask_db')
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
