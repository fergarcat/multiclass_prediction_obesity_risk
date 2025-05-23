import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "Obesity Risk Predictor"
    PROJECT_VERSION = "1.0.0"

    DB_USER = os.getenv("user")
    DB_PASSWORD = os.getenv("password")
    DB_HOST = os.getenv("host")
    DB_PORT = os.getenv("port")
    DB_NAME = os.getenv("dbname")
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()

def setup_logging(log_level):
    import logging
    logging.basicConfig(level=log_level)
