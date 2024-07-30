from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

class ApplicationConfiguration:
    SECRET_KEY = os.getenv("APP_SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('APP_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 1 day
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # 1 day
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_SECRET_KEY')
    GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
    GOOGLE_USERINFO_ENDPOINT = 'https://openidconnect.googleapis.com/v1/userinfo'
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = './sessions/'  # Directory where session files will be stored
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True 