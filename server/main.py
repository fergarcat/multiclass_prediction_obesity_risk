from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.config import settings
from .api.router import router as api_router
from .services.model_loader import load_ml_models, unload_ml_models
from .services.db_service import init_supabase_client, close_supabase_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Eventos de Inicio (Startup) ---
    print(f"INFO:     Iniciando la aplicación: {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")

    print("INFO:     Cargando modelos de Machine Learning (simulado)...")
    try:
        load_ml_models() # Llama a nuestra función (simulada)
    except Exception as e:
        print(f"CRITICAL: Fallo al cargar modelos de ML (simulado): {e}")

    print("INFO:     Inicializando cliente Supabase (simulado)...")
    try:
        await init_supabase_client() # Llama a nuestra función (simulada)
    except Exception as e:
        print(f"ERROR:    Fallo al inicializar cliente Supabase (simulado): {e}")

    yield # La aplicación se ejecuta aquí

    # --- Eventos de Apagado (Shutdown) ---
    print("INFO:     Cerrando la aplicación FastAPI...")
    unload_ml_models()
    await close_supabase_client()
    print("INFO:     Aplicación cerrada limpiamente (simulado).")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API para la predicción de riesgo de obesidad.",
    lifespan=lifespan
)

# Incluir el router de la API
app.include_router(api_router) # Aquí están nuestros endpoints como /health

@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": f"Bienvenido a {settings.PROJECT_NAME}",
        "docs": "/docs",
        "health": "/health"
    }

# Para poder ejecutar uvicorn server.main:app --reload desde la raíz del proyecto