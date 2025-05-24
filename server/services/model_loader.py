# server/services/model_loader.py
import logging
from typing import Optional
from ..core.config import settings
from ..model.prediction_model import ObesityRiskModel # Esta es tu clase actualizada

obesity_model_instance: Optional[ObesityRiskModel] = None

def load_ml_models():
    global obesity_model_instance
    try:
        # Estas rutas vienen de config.py y apuntan a los NOMBRES DE ARCHIVO ORIGINALES
        path_for_label_encoder = settings.PREPROCESSING_PIPELINE_FULL_PATH # contendrá label_encoder_nobeysdad.pkl
        path_for_model_pipeline = settings.MODEL_PIPELINE_FULL_PATH  # contendrá nuevo_pipeline_completo_v1.pkl

        if not path_for_label_encoder.exists():
            # Hacemos que el LabelEncoder (disfrazado) sea crítico también
            raise FileNotFoundError(f"Archivo LabelEncoder (esperado como '{path_for_label_encoder.name}') no encontrado: {path_for_label_encoder}")
        if not path_for_model_pipeline.exists():
            raise FileNotFoundError(f"Archivo de pipeline de modelo principal no encontrado: {path_for_model_pipeline}")
        
        logging.info(f"Cargando LabelEncoder (desde archivo '{path_for_label_encoder.name}')")
        logging.info(f"Cargando pipeline de modelo COMPLETO (desde archivo '{path_for_model_pipeline.name}')")

        obesity_model_instance = ObesityRiskModel(
            label_encoder_path=str(path_for_label_encoder), # Le pasamos el archivo que ahora es el LabelEncoder
            model_pipeline_path=str(path_for_model_pipeline) # Le pasamos el archivo que ahora es el Pipeline Completo
        )

    except Exception as e:
        logging.critical(f"ERROR CRÍTICO al cargar modelos/encoder: {e}. El servicio de predicción no estará disponible.")
        logging.exception("Detalles del error al cargar modelos/encoder:")
        obesity_model_instance = None

# Las funciones get_obesity_model_instance, unload_ml_models, are_models_loaded_successfully pueden quedar iguales.
def get_obesity_model_instance() -> ObesityRiskModel:
    if obesity_model_instance is None:
        raise RuntimeError("El modelo de obesidad y/o encoder no están cargados. El servicio de predicción no está disponible.")
    return obesity_model_instance

def unload_ml_models():
    global obesity_model_instance
    obesity_model_instance = None
    logging.info("Modelos de ML y encoder descargados.")

def are_models_loaded_successfully() -> bool:
    return obesity_model_instance is not None