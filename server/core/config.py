from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

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

settings = Settings()