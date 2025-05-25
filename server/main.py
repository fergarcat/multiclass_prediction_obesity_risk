from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from server.api.router import router as api_router
from server.services.model_loader import load_ml_models, unload_ml_models
from server.services.supabase_client import init_supabase_client  # ✅ Cambiado desde db_service
from server.core.config import setup_logging

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Iniciando aplicación. Ejecutando lifespan startup.")
    
    # Carga de modelos y cliente Supabase
    load_ml_models()
    init_supabase_client()
    
    yield

    logging.info("Apagando aplicación. Ejecutando lifespan shutdown.")
    unload_ml_models()
    # No cerramos explícitamente Supabase, ya que el cliente HTTP se maneja internamente

app = FastAPI(
    title="Multiclass Obesity Risk Prediction API",
    version="1.0.0",
    description="API para predecir el riesgo de obesidad basado en datos de salud y guardar en Supabase.",
    lifespan=lifespan
)

origins = [
    "http://localhost",
    "http://localhost:8050",
    "http://127.0.0.1:8050",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Obesity Risk Prediction API. Navigate to /docs for API documentation."}
