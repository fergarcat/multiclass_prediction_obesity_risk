# server/services/db_service.py
from ..core.config import settings
# from supabase_async_client import create_client, AsyncClient # Para cuando lo implementemos

_supabase_client = None # Placeholder para el cliente

async def init_supabase_client():
    global _supabase_client
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        print(f"INFO:    (Simulado) Intentando inicializar cliente Supabase con URL: {settings.SUPABASE_URL[:20]}...")
        # _supabase_client = await create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        _supabase_client = "Simulated Supabase Client" # Simulación
        print("INFO:    (Simulado) Cliente Supabase inicializado.")
    else:
        print("WARN:    SUPABASE_URL o SUPABASE_KEY no configurados. Funcionalidad de Supabase deshabilitada.")

async def close_supabase_client():
    global _supabase_client
    if _supabase_client:
        print("INFO:    (Simulado) Sesión de Supabase cerrada.")
        _supabase_client = None

async def get_supabase_client(): # Para inyección de dependencias
    return _supabase_client

# Placeholder para la función de guardar
# async def save_prediction_to_db(client, input_payload, prediction_result): ...
