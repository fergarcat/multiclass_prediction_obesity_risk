# server/services/prediction_service.py
import pandas as pd
from typing import Tuple # Para devolver string e índice
from ..model.prediction_model import PredictionInput # Uso de importación relativa
from .model_loader import get_preprocessing_pipeline, get_model_pipeline # Uso de importación relativa

# Define tus etiquetas de clase y su mapeo a índices si es necesario
# Esto debe coincidir con cómo fue entrenado tu modelo y lo que esperas en la DB.
# EJEMPLO:
CLASS_LABELS_LIST = [
    "Insufficient_Weight", "Normal_Weight", "Overweight_Level_I",
    "Overweight_Level_II", "Obesity_Type_I", "Obesity_Type_II", "Obesity_Type_III"
]
# Si NObeyesdad en tu DB espera un índice específico (0-6), necesitas este mapeo.
# Si tu modelo ya devuelve la etiqueta de texto, adapta esto.

async def make_prediction(input_data: PredictionInput) -> Tuple[str, int | None]: # Devuelve (categoría_string, índice_para_db)
    try:
        preprocessing_pipeline = get_preprocessing_pipeline()
        model_pipeline = get_model_pipeline()

        # Convertir Pydantic model a un diccionario, luego a DataFrame
        # Asegúrate que el orden de las columnas y los nombres sean los que espera el preprocesador
        # Usa model_dump(by_alias=True) si usaste alias en PredictionInput que coinciden con los nombres de columna originales
        input_dict = input_data.model_dump(by_alias=True) # o solo model_dump()
        input_df = pd.DataFrame([input_dict])
        print(f"DEBUG: Input DataFrame para preprocesar:\n{input_df.to_string()}")

        # Aplicar preprocesamiento
        processed_features = preprocessing_pipeline.transform(input_df)
        # El tipo de processed_features puede ser un array NumPy o una matriz dispersa
        print(f"DEBUG: Features preprocesadas (tipo: {type(processed_features)}, forma: {getattr(processed_features, 'shape', 'N/A')})")

        # Realizar predicción
        prediction_raw = model_pipeline.predict(processed_features) # Esto usualmente devuelve un array NumPy
        print(f"DEBUG: Predicción cruda del modelo: {prediction_raw}")

        # Obtener la primera predicción (asumiendo una sola muestra de entrada)
        # Y convertirla a un tipo manejable (ej. int si es un índice, o str si ya es la etiqueta)
        # AJUSTA ESTO según lo que tu `model_pipeline.predict()` realmente devuelva
        if isinstance(prediction_raw[0], (int, float)): # Si devuelve un índice numérico
            predicted_value = int(prediction_raw[0])
            if 0 <= predicted_value < len(CLASS_LABELS_LIST):
                predicted_category_string = CLASS_LABELS_LIST[predicted_value]
                predicted_index_for_db = predicted_value
            else:
                # Manejar el caso de un índice inesperado
                print(f"ERROR: Índice de predicción inesperado: {predicted_value}")
                predicted_category_string = "Unknown_Prediction"
                predicted_index_for_db = None # O un valor default si tu DB lo permite
        elif isinstance(prediction_raw[0], str): # Si ya devuelve la etiqueta de texto
            predicted_category_string = prediction_raw[0]
            # Necesitarías mapear el string a un índice para la DB si NObeyesdad es int
            try:
                predicted_index_for_db = CLASS_LABELS_LIST.index(predicted_category_string)
            except ValueError:
                print(f"ERROR: Categoría de predicción desconocida para mapear a índice: {predicted_category_string}")
                predicted_index_for_db = None
        else:
            # Tipo de predicción no esperado
            print(f"ERROR: Tipo de predicción no esperado: {type(prediction_raw[0])}")
            predicted_category_string = "Error_In_Prediction"
            predicted_index_for_db = None

        print(f"DEBUG: Categoría predicha (string): {predicted_category_string}, Índice para DB: {predicted_index_for_db}")
        return predicted_category_string, predicted_index_for_db

    except RuntimeError as e: # Ej. si los modelos no están cargados
        print(f"ERROR:   RuntimeError en make_prediction: {e}")
        raise
    except Exception as e:
        print(f"ERROR:   Excepción inesperada en make_prediction: {e}")
        import traceback
        traceback.print_exc()
        # No levantes HTTPException aquí, deja que el endpoint lo haga
        # para mantener el servicio agnóstico a HTTP.
        raise ValueError(f"Error interno al procesar la predicción: {e}") from e