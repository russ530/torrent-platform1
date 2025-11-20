import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/torrent_platform')
    DATABASE_NAME = 'torrent_platform'
    
    # JWT Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    JWT_ALGORITHM = 'HS256'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'torrent', 'txt'}
    
    # Application Configuration
    DEBUG = os.getenv('DEBUG', False)
