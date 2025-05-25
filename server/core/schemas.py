# server/core/api_schemas.py
from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    message: str

class HealthCheckResponse(BaseModel):
    status: str
    message: str
    models_loaded: bool