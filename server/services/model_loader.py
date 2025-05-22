import joblib
from pathlib import Path
from typing import Any
from ..core.config import settings # Importación relativa

_preprocessing_pipeline: Any = None
_model_pipeline: Any = None

def load_ml_models():
    global _preprocessing_pipeline, _model_pipeline
    try:
        preprocessor_path = settings.PREPROCESSING_PIPELINE_FULL_PATH
        model_path = settings.MODEL_PIPELINE_FULL_PATH

        if not preprocessor_path.exists():
            raise FileNotFoundError(f"Archivo de preprocesador no encontrado en: {preprocessor_path}")
        print(f"INFO:     Cargando preprocesador desde: {preprocessor_path}")
        _preprocessing_pipeline = joblib.load(preprocessor_path)
        print(f"INFO:     Preprocesador '{preprocessor_path.name}' cargado exitosamente.")

        if not model_path.exists():
            raise FileNotFoundError(f"Archivo de modelo no encontrado en: {model_path}")
        print(f"INFO:     Cargando modelo desde: {model_path}")
        _model_pipeline = joblib.load(model_path)
        print(f"INFO:     Modelo '{model_path.name}' cargado exitosamente.")

    except FileNotFoundError as e:
        print(f"ERROR:    {e}")
        # En un entorno de producción, podrías querer que la app no inicie si los modelos no cargan.
        # Por ahora, para desarrollo, podríamos permitir que inicie pero el endpoint de predicción fallará.
        # O puedes levantar un error para detenerlo:
        raise RuntimeError(f"Error crítico al cargar modelos: {e}. La aplicación puede no iniciar completamente.")
    except Exception as e:
        print(f"ERROR:    Error inesperado al cargar modelos: {e}")
        import traceback
        traceback.print_exc()
        raise RuntimeError(f"Error crítico al cargar modelos: {e}. La aplicación puede no iniciar completamente.")

def get_preprocessing_pipeline() -> Any:
    if _preprocessing_pipeline is None:
        # Este error no debería ocurrir si load_ml_models se llamó y fue exitoso.
        # Si load_ml_models falla y relanza una excepción, la app no debería llegar a este punto
        # o el estado de "modelos cargados" sería falso.
        raise RuntimeError("Pipeline de preprocesamiento no disponible. Verificar el inicio de la aplicación.")
    return _preprocessing_pipeline

def get_model_pipeline() -> Any:
    if _model_pipeline is None:
        raise RuntimeError("Pipeline de modelo no disponible. Verificar el inicio de la aplicación.")
    return _model_pipeline

def unload_ml_models(): # Para la fase de shutdown del lifespan
    global _preprocessing_pipeline, _model_pipeline
    _preprocessing_pipeline = None
    _model_pipeline = None
    print("INFO:     Modelos de ML (reales) liberados.")

def are_models_loaded_successfully() -> bool:
    return _preprocessing_pipeline is not None and _model_pipeline is not None