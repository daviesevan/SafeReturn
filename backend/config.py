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
    KINDE_CLIENT_ID = ""
    KINDE_CLIENT_SECRET = ""
    KINDE_REDIRECT_URL = ""
    KINDE_AUTH_URL = ""
    KINDE_TOKEN_URL = ""
    KINDE_HOST = ""
