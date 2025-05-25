# server/model/prediction_model.py
import joblib
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional, List # Asegúrate de importar List si no está
import numpy as np
import logging
from pathlib import Path
from sklearn.preprocessing import LabelEncoder

# Modelo de datos de entrada del cliente
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

# Modelo de respuesta del servidor (¡CON CAMPOS DE CONSEJO!)
class PredictionResponse(BaseModel):
    prediction: str 
    prediction_numeric: Optional[int] = None
    confidence: Optional[float] = None
    bmi: Optional[float] = None
    input_data: PredictionRequest
    tip_header: Optional[str] = None   # <--- NUEVO CAMPO PARA EL ENCABEZADO DEL CONSEJO
    tip_text: Optional[str] = None     # <--- NUEVO CAMPO PARA EL TEXTO DEL CONSEJO

class ObesityRiskModel:
    def __init__(self, label_encoder_path: str, model_pipeline_path: str):
        # `label_encoder_path` apunta al archivo que en el disco es 'preprocessing_pipeline.pkl' (que contiene el LabelEncoder).
        # `model_pipeline_path` apunta al archivo que en el disco es 'xgboost_optuna_pipeline.pkl' (que contiene tu pipeline completo).
        self.label_encoder: LabelEncoder = self._load_object(label_encoder_path, "LabelEncoder (disfrazado de preprocesador)")
        self.model_pipeline = self._load_object(model_pipeline_path, "Pipeline de Modelo Completo")
        
        logging.info("LabelEncoder y Pipeline de Modelo Completo cargados exitosamente.")
        
        if hasattr(self.model_pipeline, 'feature_names_in_'):
            logging.info(f"Pipeline principal espera las features de entrada: {list(self.model_pipeline.feature_names_in_)}")

    def _load_object(self, path: str, object_name: str):
        try:
            loaded_object = joblib.load(path)
            logging.info(f"Objeto '{object_name}' cargado exitosamente desde: {path}")
            return loaded_object
        except FileNotFoundError:
            logging.error(f"Archivo NO ENCONTRADO para '{object_name}' en {path}")
            raise RuntimeError(f"Archivo NO ENCONTRADO para objeto '{object_name}': {path}")
        except Exception as e:
            logging.error(f"Error cargando objeto '{object_name}' desde {path}: {e}")
            raise RuntimeError(f"Error cargando objeto '{object_name}': {e}")

    def calculate_bmi(self, weight_kg: float, height_m: float) -> float:
        if height_m <= 0: return 0.0
        return round(weight_kg / (height_m ** 2), 2) # Redondea BMI a 2 decimales

    def predict(self, data: PredictionRequest) -> PredictionResponse:
        input_data_dict = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        calculated_bmi = self.calculate_bmi(input_data_dict["Weight"], input_data_dict["Height"])
        input_data_dict["BMI"] = calculated_bmi
        
        df_for_pipeline = pd.DataFrame([input_data_dict])
        
        # Asegurar que las columnas están en el orden que el pipeline espera (si tiene feature_names_in_)
        if hasattr(self.model_pipeline, 'feature_names_in_'):
            try:
                # Esto es CRUCIAL: Usa una copia del df para reordenar para evitar SettingWithCopyWarning
                df_for_pipeline = df_for_pipeline.copy()[list(self.model_pipeline.feature_names_in_)]
            except KeyError as e:
                msg = (f"Error al reordenar/seleccionar columnas para el pipeline. "
                       f"Columnas disponibles: {list(df_for_pipeline.columns)}. "
                       f"Columnas esperadas por pipeline: {list(self.model_pipeline.feature_names_in_)}. Error: {e}")
                logging.error(msg)
                raise ValueError(msg) from e
        
        logging.info(f"DEBUG (server): DataFrame cols PASSED TO model_pipeline.predict(): {df_for_pipeline.columns.tolist()}")
        
        prediction_numeric_array = self.model_pipeline.predict(df_for_pipeline)
        prediction_numeric = int(prediction_numeric_array[0])
        
        prediction_label = "Etiqueta Desconocida" # Default
        try:
            prediction_label = self.label_encoder.inverse_transform([prediction_numeric])[0]
        except ValueError as ve:
             logging.error(f"Error al decodificar la predicción numérica {prediction_numeric} con LabelEncoder: {ve}. "
                           f"Clases conocidas por el LabelEncoder: {list(self.label_encoder.classes_)}")
        
        logging.info(f"Predicción numérica: {prediction_numeric}, Etiqueta decodificada: {prediction_label}")

        confidence = None
        try:
            if hasattr(self.model_pipeline, 'named_steps') and 'classifier' in self.model_pipeline.named_steps:
                classifier_step = self.model_pipeline.named_steps['classifier']
                if hasattr(classifier_step, 'predict_proba'):
                    probabilities = self.model_pipeline.predict_proba(df_for_pipeline)[0]
                    confidence = float(probabilities[prediction_numeric]) 
            elif hasattr(self.model_pipeline, 'predict_proba'): # Si el pipeline es el clasificador directamente
                 probabilities = self.model_pipeline.predict_proba(df_for_pipeline)[0]
                 confidence = float(probabilities[prediction_numeric]) 
        except Exception as e:
            logging.warning(f"No se pudo obtener predict_proba del pipeline/modelo: {e}")
        
         # --- LÓGICA DE CONSEJOS (HARDCODEADA POR AHORA) ---
        tip_header_val = "General Recommendation" # En inglés
        tip_text_val = "Maintaining a balanced diet and regular physical activity are key to a healthy lifestyle. Consult a professional for a personalized plan."

        if prediction_label == "Obesity_Type_III":
            tip_header_val = "Priority Attention!"
            tip_text_val = "Your result indicates a very high risk (Obesity Type III). It is crucial to consult with a medical specialist immediately for a comprehensive treatment plan and personalized follow-up. Do not delay seeking professional help to improve your health."
        elif prediction_label == "Obesity_Type_II":
            tip_header_val = "Important Recommendation: Obesity Type II"
            tip_text_val = "Your obesity level (Type II) requires significant lifestyle changes and possible medical intervention. We strongly recommend consulting your doctor and a nutritionist for an action plan."
        elif prediction_label == "Obesity_Type_I":
            tip_header_val = "Health Suggestion: Obesity Type I"
            tip_text_val = "You present with Obesity Type I. This is a key time to adopt healthier dietary habits and increase your physical activity. A healthcare professional can offer valuable guidance."
        elif "Overweight_Level_II" == prediction_label: # Ajustar estas etiquetas si tu modelo produce otras
            tip_header_val = "Wellness Suggestion: Overweight Level II"
            tip_text_val = "You are in Overweight Level II. Small but consistent adjustments to your diet and an increase in physical activity can make a big difference in reaching a healthy weight."
        elif "Overweight_Level_I" == prediction_label:
            tip_header_val = "Wellness Suggestion: Overweight Level I"
            tip_text_val = "Your assessment indicates Overweight Level I. Consider incorporating more vegetables and fruits into your diet and finding a physical activity you enjoy to perform regularly."
        elif prediction_label == "Normal_Weight":
            tip_header_val = "Excellent Health Status!"
            tip_text_val = "Congratulations on maintaining a Normal Weight! Continue your good eating and physical activity habits to preserve your well-being."
        elif prediction_label == "Insufficient_Weight":
            tip_header_val = "Important Consideration: Insufficient Weight"
            tip_text_val = "Your weight is below the recommended range. It's important to ensure adequate caloric and nutritional intake to maintain your energy and health. Consult a professional if you have concerns or difficulty gaining weight."
        # --- FIN DE LÓGICA DE CONSEJOS ---
            
        return PredictionResponse(
            prediction=prediction_label,
            prediction_numeric=prediction_numeric,
            confidence=confidence,
            bmi=calculated_bmi, 
            input_data=data,
            tip_header=tip_header_val, 
            tip_text=tip_text_val     
        )