from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import logging
import sys

PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent.parent



class Settings(BaseSettings):
    PROJECT_NAME: str = "API de Clasificación de Riesgo de Obesidad"
    PROJECT_VERSION: str = "0.1.0"

    # Rutas a los modelos (como strings desde el .env o defaults)
    PREPROCESSING_PIPELINE_PATH_STR: str = "data/modeling/pkl/preprocessing_pipeline.pkl"
    MODEL_PIPELINE_PATH_STR: str = "data/modeling/pkl/xgboost_optuna_pipeline.pkl"

    # Supabase
    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None
    SUPABASE_TABLE_NAME: str = "fe_obesity_risk_classification"

    # Configuración para cargar desde .env
    # Asume que .env está en la carpeta 'server/'
    model_config = SettingsConfigDict(
        env_file= PROJECT_ROOT_DIR / "server" / ".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Propiedades para obtener las rutas completas a los modelos
    # Estas rutas serán relativas al PROJECT_ROOT_DIR porque así definimos las _PATH_STR
    # y asumimos que CWD = PROJECT_ROOT_DIR al correr uvicorn.
    @property
    def PREPROCESSING_PIPELINE_FULL_PATH(self) -> Path:
        return PROJECT_ROOT_DIR / self.PREPROCESSING_PIPELINE_PATH_STR

    @property
    def MODEL_PIPELINE_FULL_PATH(self) -> Path:
        return PROJECT_ROOT_DIR / self.MODEL_PIPELINE_PATH_STR
    
# --- CONFIGURACIÓN DE LOGGING ---
LOG_DIR = PROJECT_ROOT_DIR / "server" / "logs" # Directorio para los archivos de log

def setup_logging(log_level=logging.INFO):
    LOG_DIR.mkdir(parents=True, exist_ok=True) # Crea el directorio si no existe

    # Formato del log (puedes ajustarlo si quieres diferenciar más entre tipos de log)
    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] [%(module)s:%(lineno)d] - %(message)s"
    )

    # --- Manejador de archivo ÚNICO para todos los logs ---
    # Este archivo capturará los logs de tu aplicación, errores de Uvicorn y accesos HTTP.
    unified_log_file_handler = logging.FileHandler(LOG_DIR / "app_history.log", mode='a', encoding='utf-8')
    unified_log_file_handler.setFormatter(log_formatter)
    unified_log_file_handler.setLevel(log_level) # Establece el nivel para este manejador

    # --- Configurar los loggers específicos de Uvicorn para que usen el manejador unificado ---

    # Logger para uvicorn.error (eventos del servidor, errores, startup, shutdown)
    # También usado por FastAPI para sus propios mensajes de error y de la app si no especificas otro.
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.addHandler(unified_log_file_handler) # Dirige al archivo único
    uvicorn_error_logger.setLevel(log_level) # Asegurar que el logger tiene el nivel adecuado
    # Si el logger raíz también tiene un manejador de consola,
    # y uvicorn ya loguea a consola, puedes necesitar propagate = False
    # para evitar duplicados en la consola para ESTOS mensajes específicos.
    # Si no añades un manejador de consola al logger raíz, esto puede no ser necesario.
    uvicorn_error_logger.propagate = False # Probar con y sin para ver si hay duplicados en consola

    # Logger para uvicorn.access (peticiones HTTP)
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.addHandler(unified_log_file_handler) # Dirige al archivo único
    uvicorn_access_logger.setLevel(log_level)
    uvicorn_access_logger.propagate = False # Probar con y sin para ver si hay duplicados en consola

    # --- Configurar el logger raíz ---
    # Para capturar logs de tu aplicación (logging.info(), logging.error() desde tus módulos)
    # y logs de otras librerías que no sean uvicorn.
    root_logger = logging.getLogger() # Obtiene el logger raíz
    root_logger.addHandler(unified_log_file_handler) # También envía los logs raíz al archivo único
    root_logger.setLevel(log_level) # Establece el nivel para el logger raíz

    # --- Manejador de consola (Importante para ver logs en la terminal) ---
    # Uvicorn ya añade su propio manejador de consola, pero si lo deshabilitas
    # con propagate=False para uvicorn.error y uvicorn.access, necesitas uno
    # en el logger raíz si quieres seguir viendo TODOS los logs en consola.
    # Si dejas que uvicorn maneje la consola para sus logs, y solo quieres que TUS
    # logs de app vayan a consola también (además del archivo), puedes añadirlo al root_logger.

    # Si estableciste propagate=False arriba, este manejador de consola es más importante
    # para asegurar que los mensajes (incluidos los de uvicorn) sigan apareciendo en la consola.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter) # Usa el mismo formato o uno más simple
    console_handler.setLevel(log_level)
    # Añadirlo al logger raíz es una forma de asegurar que todos los logs (incluidos los propagados) lo usen
    # pero podría causar duplicados si los loggers de uvicorn no tienen propagate=False
    # y ya tienen su propio manejador de consola.
    # Si los loggers de uvicorn tienen propagate=False, entonces necesitas que el logger raíz
    # tenga un manejador de consola si quieres verlos allí.
    # Vamos a añadirlo al logger raíz. Si ves duplicados en consola, entonces el propagate=False
    # en los loggers de uvicorn está funcionando bien y puedes quitarlo aquí si prefieres
    # el formato de consola por defecto de uvicorn.
    # root_logger.addHandler(console_handler) # DESCOMENTA ESTO si con propagate=False arriba no ves logs de uvicorn en consola

    # O, para controlar mejor, solo añade el manejador de consola a tu propio logger de app,
    # y deja que uvicorn maneje su propia salida a consola.
    # app_logger = logging.getLogger("tu_nombre_de_app_aqui_o_el_raiz_si_quieres_todo")
    # app_logger.addHandler(console_handler)

    # Mensaje de confirmación
    confirm_logger = logging.getLogger(__name__)
    confirm_logger.info(f"Logging configurado (unificado). Nivel: {logging.getLevelName(log_level)}. Archivo: {LOG_DIR / 'app_history.log'}")

settings = Settings()