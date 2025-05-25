# client/config/client_settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class ClientSettings(BaseSettings):
    FASTAPI_PREDICTION_URL: str = "http://127.0.0.1:8000/prediction"

    class Config:
        env_file = PROJECT_ROOT_DIR / ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'

client_settings = ClientSettings()