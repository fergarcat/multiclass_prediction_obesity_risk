# server/services/model_loader.py
import joblib
from pathlib import Path
from typing import Any, Optional
from ..core.config import settings
from ..model.prediction_model import ObesityRiskModel # Importa la clase del modelo que definimos
import logging

# Instancia global del modelo de ML
obesity_model_instance: Optional[ObesityRiskModel] = None

def load_ml_models():
    """Carga los modelos ML y crea una instancia de ObesityRiskModel."""
    global obesity_model_instance
    try:
        preprocessing_path = settings.PREPROCESSING_PIPELINE_FULL_PATH
        model_path = settings.MODEL_PIPELINE_FULL_PATH

        if not preprocessing_path.exists():
            raise FileNotFoundError(f"Archivo de preprocesador no encontrado: {preprocessing_path}")
        if not model_path.exists():
            raise FileNotFoundError(f"Archivo de modelo no encontrado: {model_path}")
        
        logging.info(f"Cargando preprocesador desde: {preprocessing_path}")
        logging.info(f"Cargando modelo desde: {model_path}")

        # Aquí creamos la instancia de tu ObesityRiskModel pasándole las rutas
        obesity_model_instance = ObesityRiskModel(preprocessing_pipeline_path=str(preprocessing_path), 
                                                model_pipeline_path=str(model_path))
        logging.info("Todos los modelos cargados y la instancia de ObesityRiskModel está lista.")

    except (FileNotFoundError, RuntimeError) as e:
        logging.critical(f"ERROR CRÍTICO al cargar modelos: {e}. El servicio de predicción no estará disponible.")
        # Podemos re-lanzar o simplemente dejar la instancia como None.
        # Para FastAPI Lifespan, es mejor manejarlo suavemente si la app puede arrancar sin ello,
        # pero para el endpoint de predicción habrá un 503.
        obesity_model_instance = None 
    except Exception as e:
        logging.critical(f"ERROR INESPERADO al cargar modelos: {e}")
        logging.exception("Detalles del error al cargar modelos:") # Imprime el stack trace
        obesity_model_instance = None


def get_obesity_model_instance() -> ObesityRiskModel:
    """Devuelve la instancia global del modelo de ML. Lanza un error si no está cargada."""
    if obesity_model_instance is None:
        raise RuntimeError("El modelo de obesidad no está cargado. El servicio de predicción no está disponible.")
    return obesity_model_instance

def unload_ml_models():
    """Libera los modelos de la memoria."""
    global obesity_model_instance
    obesity_model_instance = None
    logging.info("Modelos de ML descargados.")

def are_models_loaded_successfully() -> bool:
    """Comprueba si los modelos están cargados."""
    return obesity_model_instance is not None