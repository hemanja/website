import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ycsleeve-geo-2024-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ycsleeve.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Company info for GEO
    COMPANY_NAME = "YC INSULATION"
    COMPANY_FULL_NAME = "佛山盈灿绝缘材料有限公司"
    COMPANY_EMAIL = "heman508@gmail.com"
    COMPANY_PHONE = "+86 180 2224 0398"
    COMPANY_WHATSAPP = "+86 135 9060 5550"
    COMPANY_ADDRESS = "佛山市顺德区陈村镇永兴工业区2路"
    COMPANY_FOUNDED = "2008"
    COMPANY_CERTIFICATIONS = ["UL", "VDE", "SGS", "RoHS", "REACH"]
