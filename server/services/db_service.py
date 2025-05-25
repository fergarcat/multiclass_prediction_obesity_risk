from ..core.config import settings 
from ..model.prediction_model import PredictionResponse
import logging
import pandas as pd
from typing import Optional

# Mapas para DB
gender_db_map = {"Male": 1, "Female": 0}
binary_db_map = {"yes": 1, "no": 0}
caec_db_map = {"Always": 3, "Frequently": 2, "Sometimes": 1, "no": 0}
calc_db_map = {"Always": 3, "Frequently": 2, "Sometimes": 1, "no": 0}
mtrans_db_map = {
    "Public_Transportation": 0,
    "Walking": 1,
    "Automobile": 2,
    "Bike": 3,
    "Motorbike": 4
}

nobeyesdad_label_to_int_map = {
    "Insufficient_Weight": 0, "Normal_Weight": 1, "Overweight_Level_I": 2,
    "Overweight_Level_II": 3, "Obesity_Type_I": 4, "Obesity_Type_II": 5, "Obesity_Type_III": 6
}

async def save_prediction_to_db(prediction_data: PredictionResponse):
    try:
        # Import diferido para evitar errores de inicialización
        from .supabase_client import get_supabase_client
        supabase_client_instance = get_supabase_client()
        input_payload = prediction_data.input_data

        nobeyesdad_value = -1
        if isinstance(prediction_data.prediction, (int, float)) or \
           (isinstance(prediction_data.prediction, str) and prediction_data.prediction.isdigit()):
            try:
                nobeyesdad_value = int(prediction_data.prediction)
                logging.info(f"Predicción '{prediction_data.prediction}' convertida a entero {nobeyesdad_value}.")
            except ValueError:
                logging.warning(f"No se pudo convertir la predicción '{prediction_data.prediction}' a entero.")

        if nobeyesdad_value == -1:
            nobeyesdad_value = nobeyesdad_label_to_int_map.get(str(prediction_data.prediction), -1)
            logging.info(f"Predicción '{prediction_data.prediction}' mapeada a {nobeyesdad_value}.")

        data_to_insert = {
            "gender": gender_db_map.get(input_payload.Gender, -1),
            "age": input_payload.Age,
            "height": int(round(input_payload.Height)),
            "weight": int(round(input_payload.Weight)),
            "family_history_with_overweight": binary_db_map.get(input_payload.Family_History_with_Overweight, -1),
            "favc": binary_db_map.get(input_payload.FAVC, -1),
            "fcvc": int(round(input_payload.FCVC)),
            "ncp": int(round(input_payload.NCP)),
            "caec": caec_db_map.get(input_payload.CAEC, -1),
            "smoking": binary_db_map.get(input_payload.SMOKING, -1),
            "ch2o": int(round(input_payload.CH2O)),
            "scc": binary_db_map.get(input_payload.SCC, -1),
            "faf": int(round(input_payload.FAF)),
            "tue": int(round(input_payload.TUE)),
            "calc": calc_db_map.get(input_payload.CALC, -1),
            "mtrans": mtrans_db_map.get(input_payload.MTRANS, -1),
            "nobeyesdad": nobeyesdad_value,
            "bmi": prediction_data.bmi,
            "created_at": pd.Timestamp.now(tz='UTC').isoformat()
        }

        logging.info(f"Payload FINAL para inserción en Supabase: {data_to_insert}")

        response = supabase_client_instance.table(settings.SUPABASE_TABLE_NAME).insert(data_to_insert).execute()

        if hasattr(response, 'data') and response.data:
            logging.info(f"✅ Predicción guardada. Registros insertados: {len(response.data)}")
        else:
            logging.info(f"✅ Guardado completado. Respuesta: {response}")
    except Exception as e:
        logging.error(f"❌ Error al guardar predicción en Supabase: {e}")
        logging.exception("Detalles del error:")

async def get_tip_by_prediction_value(prediction_numeric_value: int) -> Optional[dict]:
    try:
        from .supabase_client import get_supabase_client
        supabase = get_supabase_client()

        TIPS_TABLE_NAME = "tip_text"
        response = supabase.table(TIPS_TABLE_NAME)\
            .select("description, detailed_advice")\
            .eq("id", prediction_numeric_value)\
            .maybe_single().execute()

        if response.data:
            logging.info(f"Consejo encontrado: {response.data}")
            return {
                "tip_header": response.data.get("description", "Consejo"),
                "tip_text": response.data.get("detailed_advice", "Sin detalles.")
            }
        else:
            logging.warning(f"No se encontró consejo para id {prediction_numeric_value}.")
            return {"tip_header": "Consejo No Encontrado", "tip_text": "No hay consejo disponible para este resultado."}
    except Exception as e:
        logging.error(f"❌ Error al obtener consejo para id {prediction_numeric_value}: {e}")
        logging.exception("Detalles del error:")
        return {"tip_header": "Error de Consejos", "tip_text": "No se pudieron cargar recomendaciones."}
