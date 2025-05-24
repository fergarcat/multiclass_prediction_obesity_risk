# server/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager # Nuevo para el lifespan
import logging

from server.api.router import router as api_router
from server.services.model_loader import load_ml_models, unload_ml_models
from server.services.db_service import init_supabase_client, close_supabase_client
from server.core.config import setup_logging # Para configurar logging al inicio

# Configura el logging al inicio de la aplicación
setup_logging()

# Usa asynccontextmanager para manejar los recursos al inicio y cierre de la app
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Iniciando aplicación. Ejecutando lifespan startup.")
    # Cargar modelos ML
    load_ml_models()
    # Inicializar cliente Supabase
    await init_supabase_client()
    yield # Aquí la aplicación está "viva" y manejando solicitudes
    logging.info("Apagando aplicación. Ejecutando lifespan shutdown.")
    # Liberar recursos
    unload_ml_models()
    await close_supabase_client()

app = FastAPI(
    title="Multiclass Obesity Risk Prediction API",
    version="1.0.0",
    description="API para predecir el riesgo de obesidad basado en datos de salud y guardar en Supabase.",
    lifespan=lifespan # Integra el lifespan aquí
)

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8050", # El puerto predeterminado de Dash
    "http://127.0.0.1:8050",
    "*" # Para desarrollo, permite todos los orígenes. AJUSTA EN PRODUCCIÓN.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router) # Ahora usamos api_router que es el nombre correcto

@app.get("/")
async def root():
    return {"message": "Welcome to the Obesity Risk Prediction API. Navigate to /docs for API documentation."}