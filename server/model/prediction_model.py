# server/model/prediction_model.py
import joblib
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional
import numpy as np
import logging
from pathlib import Path
from sklearn.preprocessing import LabelEncoder # Importar para type hinting si es necesario

# Modelo de datos de entrada del cliente (COINCIDE CON LO QUE TU PIPELINE COMPLETO ESPERA)
class PredictionRequest(BaseModel):
    Gender: str
    Age: int = Field(..., gt=0, lt=100)
    Height: float = Field(..., gt=1.0, lt=2.5)
    Weight: float = Field(..., gt=30.0, lt=200.0)
    Family_History_with_Overweight: str
    FAVC: str
    FCVC: float = Field(..., gt=0.0, lt=4.0)
    NCP: float = Field(..., gt=0.0, lt=5.0)
    CAEC: str
    SMOKING: str
    CH2O: float = Field(..., gt=0.0, lt=4.0)
    SCC: str
    FAF: float = Field(..., gt=0.0, lt=4.0)
    TUE: float = Field(..., ge=0.0, lt=4.0)
    CALC: str
    MTRANS: str
    # BMI no se incluye aquí porque lo calcularemos y lo añadiremos antes de pasar al pipeline

# Modelo de respuesta del servidor
class PredictionResponse(BaseModel):
    prediction: str # Etiqueta STRING decodificada
    prediction_numeric: Optional[int] = None # El valor numérico de la predicción (del LabelEncoder)
    confidence: Optional[float] = None
    bmi: Optional[float] = None
    input_data: PredictionRequest

class ObesityRiskModel:
    def __init__(self, label_encoder_path: str, model_pipeline_path: str):
        # `label_encoder_path` ahora apunta al archivo que TUS COMPAÑEROS conocen como "preprocessing_pipeline.pkl",
        # pero que para nosotros contiene el LabelEncoder.
        # `model_pipeline_path` apunta al archivo que TUS COMPAÑEROS conocen como "xgboost_optuna_pipeline.pkl",
        # pero que para nosotros contiene tu nuevo pipeline COMPLETO.

        self.label_encoder = self._load_object(label_encoder_path, "LabelEncoder")
        self.model_pipeline = self._load_object(model_pipeline_path, "Pipeline de Modelo Completo")
        
        logging.info("LabelEncoder (cargado como 'preprocessing_pipeline.pkl') y Pipeline de Modelo Completo (cargado como 'xgboost_optuna_pipeline.pkl') cargados exitosamente.")
        
        if hasattr(self.model_pipeline, 'feature_names_in_'):
            logging.info(f"Pipeline principal espera las features de entrada: {list(self.model_pipeline.feature_names_in_)}")

    def _load_object(self, path: str, object_name: str): # Función genérica para cargar .pkl
        try:
            loaded_object = joblib.load(path)
            logging.info(f"Objeto '{object_name}' cargado exitosamente desde: {path}")
            return loaded_object
        except Exception as e:
            logging.error(f"Error cargando objeto '{object_name}' desde {path}: {e}")
            raise RuntimeError(f"Error cargando objeto '{object_name}': {e}")

    def calculate_bmi(self, weight_kg: float, height_m: float) -> float:
        if height_m <= 0: return 0.0
        return weight_kg / (height_m ** 2)

    def predict(self, data: PredictionRequest) -> PredictionResponse:
        input_data_dict = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        calculated_bmi = self.calculate_bmi(input_data_dict["Weight"], input_data_dict["Height"])
        input_data_dict["BMI"] = calculated_bmi
        
        df_for_pipeline = pd.DataFrame([input_data_dict])
        
        # Asegurar que las columnas están en el orden que el pipeline espera (si tiene feature_names_in_)
        if hasattr(self.model_pipeline, 'feature_names_in_'):
            try:
                df_for_pipeline = df_for_pipeline[self.model_pipeline.feature_names_in_]
            except KeyError as e:
                msg = (f"Error al reordenar/seleccionar columnas para el pipeline. "
                       f"Columnas disponibles: {list(df_for_pipeline.columns)}. "
                       f"Columnas esperadas por pipeline: {list(self.model_pipeline.feature_names_in_)}. Error: {e}")
                logging.error(msg)
                raise ValueError(msg) from e
        
        logging.info(f"DEBUG (server): DataFrame cols PASSED TO model_pipeline.predict(): {df_for_pipeline.columns.tolist()}")
        # print(f"DEBUG (server): Muestra de datos ANTES de model_pipeline.predict():\n{df_for_pipeline.head(1).to_dict(orient='records')}")

        # Usamos DIRECTAMENTE self.model_pipeline (tu nuevo_pipeline_completo_v1.pkl renombrado)
        prediction_numeric_array = self.model_pipeline.predict(df_for_pipeline)
        prediction_numeric = int(prediction_numeric_array[0])
        
        # Usamos self.label_encoder (tu label_encoder_nobeysdad.pkl renombrado)
        prediction_label = self.label_encoder.inverse_transform([prediction_numeric])[0]
        
        logging.info(f"Predicción numérica: {prediction_numeric}, Etiqueta decodificada: {prediction_label}")

        confidence = None
        try:
            # Acceder al clasificador XGBoost DENTRO del pipeline para predict_proba
            if hasattr(self.model_pipeline, 'named_steps') and 'classifier' in self.model_pipeline.named_steps:
                classifier_step = self.model_pipeline.named_steps['classifier']
                if hasattr(classifier_step, 'predict_proba'):
                    probabilities = self.model_pipeline.predict_proba(df_for_pipeline)[0]
                    confidence = probabilities[prediction_numeric] 
            else: # Si es el clasificador directamente (menos probable si es un pipeline complejo)
                if hasattr(self.model_pipeline, 'predict_proba'):
                     probabilities = self.model_pipeline.predict_proba(df_for_pipeline)[0]
                     confidence = probabilities[prediction_numeric] 
        except Exception as e:
            logging.warning(f"No se pudo obtener predict_proba del pipeline/modelo: {e}")
            
        return PredictionResponse(
            prediction=prediction_label,
            prediction_numeric=prediction_numeric,
            confidence=confidence,
            bmi=calculated_bmi,
            input_data=data
        )