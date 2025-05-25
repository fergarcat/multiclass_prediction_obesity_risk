# server/services/supabase_client.py

from supabase import create_client, Client
from server.core.config import settings
import logging

supabase: Client | None = None  # Usa 'supabase' sin guión bajo

def init_supabase_client():
    global supabase
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        try:
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            logging.info("✅ Cliente de Supabase inicializado correctamente.")
        except Exception as e:
            logging.error(f"❌ Error al inicializar el cliente de Supabase: {e}", exc_info=True)
    else:
        logging.warning("⚠️ No se encontraron SUPABASE_URL o SUPABASE_KEY en las variables de entorno.")

def get_supabase_client() -> Client:
    if supabase is None:
        logging.warning("⚠️ Supabase client aún no está inicializado.")
        raise RuntimeError("Supabase client no inicializado o configurado. La conexión DB no está disponible.")
    return supabase
