# server/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import logging
import sys

PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent.parent # Esto debería apuntar a multiclass_prediction_obesity_risk/

class Settings(BaseSettings):
    PROJECT_NAME: str = "API de Clasificación de Riesgo de Obesidad"
    PROJECT_VERSION: str = "0.1.0"

    PREPROCESSING_PIPELINE_PATH_STR: str = "server/data/modeling/pkl/preprocessing_pipeline.pkl" # Ruta relativa a PROJECT_ROOT_DIR
    MODEL_PIPELINE_PATH_STR: str = "server/data/modeling/pkl/xgboost_optuna_pipeline.pkl" # Ruta relativa a PROJECT_ROOT_DIR

    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None
    SUPABASE_TABLE_NAME: str = "fe_obesity_risk_classification"

    # Configuración para cargar desde .env en la RAÍZ del proyecto
    model_config = SettingsConfigDict(
        env_file= PROJECT_ROOT_DIR / ".env", # Busca .env en la raíz (multiclass_prediction_obesity_risk/.env)
        env_file_encoding='utf-8',
        extra='ignore'
    )

    @property
    def PREPROCESSING_PIPELINE_FULL_PATH(self) -> Path:
        return self.PROJECT_ROOT_DIR / self.PREPROCESSING_PIPELINE_PATH_STR

    @property
    def MODEL_PIPELINE_FULL_PATH(self) -> Path:
        return self.PROJECT_ROOT_DIR / self.MODEL_PIPELINE_PATH_STR
    
    # Añadimos una propiedad para PROJECT_ROOT_DIR dentro de Settings si la necesitas en otras partes
    @property
    def PROJECT_ROOT_DIR(self) -> Path:
        return PROJECT_ROOT_DIR # Usa la variable global ya definida

# --- CONFIGURACIÓN DE LOGGING (no cambia) ---
# ... (Tu código de logging actual de config.py es válido aquí) ...
LOG_DIR = PROJECT_ROOT_DIR / "server" / "logs" # Directorio para los archivos de log

def setup_logging(log_level=logging.INFO):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] [%(module)s:%(lineno)d] - %(message)s"
    )

    unified_log_file_handler = logging.FileHandler(LOG_DIR / "app_history.log", mode='a', encoding='utf-8')
    unified_log_file_handler.setFormatter(log_formatter)
    unified_log_file_handler.setLevel(log_level)

    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.addHandler(unified_log_file_handler)
    uvicorn_error_logger.setLevel(log_level)
    uvicorn_error_logger.propagate = False

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.addHandler(unified_log_file_handler)
    uvicorn_access_logger.setLevel(log_level)
    uvicorn_access_logger.propagate = False

    root_logger = logging.getLogger()
    root_logger.addHandler(unified_log_file_handler)
    root_logger.setLevel(log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(log_level)
    # root_logger.addHandler(console_handler) # Descomentar si necesitas logs en consola si uvicorn.propagate=False

    confirm_logger = logging.getLogger(__name__)
    confirm_logger.info(f"Logging configurado (unificado). Nivel: {logging.getLevelName(log_level)}. Archivo: {LOG_DIR / 'app_history.log'}")

settings = Settings()