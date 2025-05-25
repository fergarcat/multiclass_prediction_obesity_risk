# server/services/db_service.py
from ..core.config import settings
from ..model.prediction_model import PredictionResponse
import logging
import pandas as pd
from supabase import create_client, Client
from typing import Optional

_supabase_client: Client | None = None

# ====================================================================
# MAPAS DE CONVERSIÓN PARA LA BASE DE DATOS
# ====================================================================
gender_db_map = {"Male": 1, "Female": 0} 
binary_db_map = {"yes": 1, "no": 0}      
caec_db_map = {"Always": 3, "Frequently": 2, "Sometimes": 1, "no": 0} 
calc_db_map = {"Always": 3, "Frequently": 2, "Sometimes": 1, "no": 0} 

# *** NUEVO MAPA PARA MTRANS ***
# Asegúrate de que estos números (0-4) son los que quieres para tu análisis o lógica de DB.
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
# ====================================================================


async def init_supabase_client():
    global _supabase_client
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        try:
            _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            logging.info(f"Cliente Supabase REAL inicializado con URL: {settings.SUPABASE_URL[:30]}...")
        except Exception as e:
            logging.error(f"Error inicializando cliente Supabase: {e}")
            _supabase_client = None
    else:
        logging.warning("SUPABASE_URL o SUPABASE_KEY no configurados. La funcionalidad de SupABASE está deshabilitada.") # Corrección de SUPABASE
        _supabase_client = None

async def close_supabase_client():
    global _supabase_client
    if _supabase_client:
        logging.info("Cerrando conexión Supabase.")
        _supabase_client = None

def get_supabase_client() -> Client:
    if _supabase_client is None:
        raise RuntimeError("Supabase client no inicializado o configurado. La conexión DB no está disponible.")
    return _supabase_client

async def save_prediction_to_db(prediction_data: PredictionResponse):
    supabase_client_instance = get_supabase_client()
    input_payload = prediction_data.input_data

    try:
        nobeyesdad_value = -1 
        if isinstance(prediction_data.prediction, (int, float)) or \
           (isinstance(prediction_data.prediction, str) and prediction_data.prediction.isdigit()):
            try:
                nobeyesdad_value = int(prediction_data.prediction)
                logging.info(f"Predicción '{prediction_data.prediction}' convertida a entero {nobeyesdad_value} para columna 'nobeyesdad'.")
            except ValueError:
                logging.warning(f"No se pudo convertir la predicción '{prediction_data.prediction}' a entero directamente.")
        
        if nobeyesdad_value == -1: 
            nobeyesdad_value = nobeyesdad_label_to_int_map.get(str(prediction_data.prediction), -1)
            logging.info(f"Predicción '{prediction_data.prediction}' mapeada a {nobeyesdad_value} usando nobeyesdad_label_to_int_map.")

        # Las CLAVES ("gender", "age", etc.) DEBEN coincidir con los nombres de columna en tu tabla de Supabase.
        # La estructura de tu tabla Supabase que me mostraste usa snake_case (ej. family_history_with_overweight)
        # o a veces solo una palabra en minúsculas (ej. gender, age, height, weight, mtrans).
        # VOY A USAR MINÚSCULAS PARA TODAS LAS CLAVES que corresponden a las columnas de tu tabla.
        data_to_insert = {
            "gender": gender_db_map.get(input_payload.Gender, -1),
            "age": input_payload.Age,
            "height": int(round(input_payload.Height)), # Tu tabla Supabase lo tiene como 'smallint'
            "weight": int(round(input_payload.Weight)), # Tu tabla Supabase lo tiene como 'integer'
            "family_history_with_overweight": binary_db_map.get(input_payload.Family_History_with_Overweight, -1),
            "favc": binary_db_map.get(input_payload.FAVC, -1),
            "fcvc": int(round(input_payload.FCVC)), # Tu tabla Supabase es 'integer'
            "ncp": int(round(input_payload.NCP)),   # Tu tabla Supabase es 'integer'
            "caec": caec_db_map.get(input_payload.CAEC, -1), # Tu tabla Supabase es 'smallint'
            "smoking": binary_db_map.get(input_payload.SMOKING, -1), # Tu tabla Supabase es 'integer'
            "ch2o": int(round(input_payload.CH2O)),  # Tu tabla Supabase es 'integer'
            "scc": binary_db_map.get(input_payload.SCC, -1), # Tu tabla Supabase es 'integer'
            "faf": int(round(input_payload.FAF)),    # Tu tabla Supabase es 'integer'
            "tue": int(round(input_payload.TUE)),    # Tu tabla Supabase es 'integer'
            "calc": calc_db_map.get(input_payload.CALC, -1), # Tu tabla Supabase es 'smallint'
            
            # *** APLICANDO EL MAPA PARA MTRANS ***
            "mtrans": mtrans_db_map.get(input_payload.MTRANS, -1), # Convierte string a int. Tu tabla Supabase es 'integer'.
            
            "nobeyesdad": nobeyesdad_value, # Tu tabla Supabase es 'smallint'
            "bmi": prediction_data.bmi, # Tu tabla Supabase es 'double precision', así que float está bien.
            "created_at": pd.Timestamp.now(tz='UTC').isoformat()
        }
        
        logging.info(f"Preparando inserción en Supabase (tabla '{settings.SUPABASE_TABLE_NAME}'). Payload FINAL: {data_to_insert}")
        # print(f"DEBUG (server/db_service): Payload FINAL enviado a Supabase: {data_to_insert}")

        response = supabase_client_instance.table(settings.SUPABASE_TABLE_NAME).insert(data_to_insert).execute()
        
        if hasattr(response, 'data') and response.data:
            logging.info(f"Predicción guardada en Supabase. Registros insertados: {len(response.data)}")
        else:
            logging.info(f"Guardado en Supabase completado (o sin error de API). Respuesta: {response}")

    except Exception as e:
        logging.error(f"Error CRÍTICO al guardar predicción en Supabase: {e}")
        logging.exception("Detalles del error al guardar en Supabase (save_prediction_to_db):")

# server/services/db_service.py (AÑADE ESTA FUNCIÓN)
# ... (resto del archivo como lo tienes) ...

async def get_tip_by_prediction_value(prediction_numeric_value: int) -> Optional[dict]:
    """
    Obtiene un consejo de Supabase basado en el valor numérico de la predicción.
    Asume que tienes una tabla (ej. 'obesity_level_tips') con una columna 
    que coincide con 'prediction_numeric_value' (ej. 'level_id')
    y columnas para el consejo (ej. 'tip_header', 'tip_message').
    """
    supabase = get_supabase_client() # Tu función existente para obtener el cliente
    
    # >>> AJUSTA ESTOS NOMBRES DE TABLA Y COLUMNAS <<<
    TIPS_TABLE_NAME = "tip_text" # El nombre de tu tabla de consejos con ID y DESCRIPTION
    ID_COLUMN_IN_TIPS_TABLE = "id" # La columna en tu tabla de tips que tiene (1, 2, ..., 7)
    HEADER_COLUMN_NAME_IN_TIPS_TABLE = "description" # La columna que quieres como header (era "description" en tu imagen)
    TEXT_COLUMN_NAME_IN_TIPS_TABLE = "detailed_advice" #  NECESITAS UNA COLUMNA CON EL TEXTO DEL CONSEJO
                                                       # O puedes usar la misma "description" para ambos si es corta.

    if not TIPS_TABLE_NAME or not ID_COLUMN_IN_TIPS_TABLE or not TEXT_COLUMN_NAME_IN_TIPS_TABLE:
        logging.warning("Nombres de tabla/columna de consejos no configurados para Supabase.")
        return {"tip_header": "Recomendación General", "tip_text": "Consulte a un profesional para más detalles."}

    try:
        # .eq(columna_id_en_tabla_tips, valor_numerico_prediccion)
        # .select("columna_header, columna_texto_consejo")
        # .maybe_single() devuelve el primer registro o None si no hay coincidencias
        response = supabase.table(TIPS_TABLE_NAME)\
                           .select(f"{HEADER_COLUMN_NAME_IN_TIPS_TABLE}, {TEXT_COLUMN_NAME_IN_TIPS_TABLE}")\
                           .eq(ID_COLUMN_IN_TIPS_TABLE, prediction_numeric_value)\
                           .maybe_single().execute()

        if response.data:
            logging.info(f"Consejo encontrado para prediction_id {prediction_numeric_value}: {response.data}")
            # Asegúrate de que las claves del diccionario devuelto coincidan con lo que espera PredictionResponse
            return {
                "tip_header": response.data.get(HEADER_COLUMN_NAME_IN_TIPS_TABLE, "Consejo"),
                "tip_text": response.data.get(TEXT_COLUMN_NAME_IN_TIPS_TABLE, "Información no disponible.")
            }
        else:
            logging.warning(f"No se encontró consejo para prediction_id {prediction_numeric_value} en la tabla '{TIPS_TABLE_NAME}'.")
            return {"tip_header": "Consejo No Encontrado", "tip_text": "No hay un consejo específico para este resultado en la base de datos."}
            
    except Exception as e:
        logging.error(f"Error obteniendo consejo de Supabase para prediction_id {prediction_numeric_value}: {e}")
        logging.exception("Detalles del error de Supabase al obtener consejo:")
        return {"tip_header": "Error de Consejos", "tip_text": "No se pudieron cargar las recomendaciones en este momento."}