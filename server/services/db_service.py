# server/services/db_service.py
from ..core.config import settings
from ..model.prediction_model import PredictionResponse
import logging
import pandas as pd
from supabase import create_client, Client # Asegúrate que 'supabase' está instalado

_supabase_client: Client | None = None

# ====================================================================
# MAPAS DE CONVERSIÓN PARA LA BASE DE DATOS
# ====================================================================
gender_db_map = {"Male": 1, "Female": 0} 
binary_db_map = {"yes": 1, "no": 0}      
caec_db_map = {"Always": 3, "Frequently": 2, "Sometimes": 1, "no": 0} 
calc_db_map = {"Always": 3, "Frequently": 2, "Sometimes": 1, "no": 0} 

nobeyesdad_label_to_int_map = { 
    "Insufficient_Weight": 0,
    "Normal_Weight": 1,
    "Overweight_Level_I": 2,
    "Overweight_Level_II": 3,
    "Obesity_Type_I": 4,
    "Obesity_Type_II": 5,
    "Obesity_Type_III": 6
}
# ====================================================================


async def init_supabase_client():
    """Inicializa el cliente de Supabase."""
    global _supabase_client
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        try:
            _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            logging.info(f"Cliente Supabase REAL inicializado con URL: {settings.SUPABASE_URL[:30]}...")
        except Exception as e:
            logging.error(f"Error inicializando cliente Supabase: {e}")
            _supabase_client = None
    else:
        logging.warning("SUPABASE_URL o SUPABASE_KEY no configurados. La funcionalidad de Supabase está deshabilitada.")
        _supabase_client = None

async def close_supabase_client():
    """Cierra la conexión con Supabase."""
    global _supabase_client
    if _supabase_client:
        logging.info("Cerrando conexión Supabase.")
        _supabase_client = None

def get_supabase_client() -> Client:
    if _supabase_client is None:
        raise RuntimeError("Supabase client no inicializado o configurado. La conexión DB no está disponible.")
    return _supabase_client

async def save_prediction_to_db(prediction_data: PredictionResponse):
    """
    Guarda la predicción en la tabla de Supabase, asegurando que los tipos de datos
    coincidan con el schema de la tabla (especialmente para integers/smallints).
    """
    supabase_client_instance = get_supabase_client()
    input_payload = prediction_data.input_data

    try:
        # Determinar el valor para 'nobeyesdad'
        nobeyesdad_value = -1 # Valor por defecto si no se puede convertir/mapear
        if isinstance(prediction_data.prediction, (int, float)) or \
           (isinstance(prediction_data.prediction, str) and prediction_data.prediction.isdigit()):
            try:
                nobeyesdad_value = int(prediction_data.prediction)
                logging.info(f"Predicción '{prediction_data.prediction}' convertida a entero {nobeyesdad_value} para columna 'nobeyesdad'.")
            except ValueError:
                logging.warning(f"No se pudo convertir la predicción '{prediction_data.prediction}' a entero directamente.")
        
        if nobeyesdad_value == -1: # Si no fue un número directo o falló la conversión
            nobeyesdad_value = nobeyesdad_label_to_int_map.get(str(prediction_data.prediction), -1)
            logging.info(f"Predicción '{prediction_data.prediction}' mapeada a {nobeyesdad_value} usando nobeyesdad_label_to_int_map.")


        # Preparar los datos para insertar, asegurando los tipos correctos para Supabase
        # Las CLAVES deben ser los NOMBRES DE COLUMNA EXACTOS de tu tabla Supabase.
        # Si tu tabla Supabase tiene nombres de columna en minúsculas (ej. 'height'), usa minúsculas.
        # Si son PascalCase ('Height'), usa PascalCase. Basado en tu error anterior de Supabase,
        # parece que espera minúsculas, por ej. "height". Voy a asumir minúsculas aquí.
        # ¡VERIFICA ESTO CONTRA TU TABLA REAL `fe_obesity_risk_classification`!
        data_to_insert = {
            "gender": gender_db_map.get(input_payload.Gender, -1),
            "age": input_payload.Age, # Pydantic ya lo tiene como int
            
            # Para columnas que son float en Pydantic PERO integer/smallint en Supabase:
            "height": int(round(input_payload.Height)), 
            "weight": int(round(input_payload.Weight)), # Si 'weight' es double precision en DB, quita int(round(...))
            
            "family_history_with_overweight": binary_db_map.get(input_payload.Family_History_with_Overweight, -1),
            "favc": binary_db_map.get(input_payload.FAVC, -1),
            "fcvc": int(round(input_payload.FCVC)),
            "ncp": int(round(input_payload.NCP)),
            "caec": caec_db_map.get(input_payload.CAEC, -1),
            "smoking": binary_db_map.get(input_payload.SMOKING, -1),
            "ch2o": int(round(input_payload.CH2O)),
            "scc": binary_db_map.get(input_payload.SCC, -1),
            "faf": int(round(input_payload.FAF)),
            "tue": int(round(input_payload.TUE)), # Pydantic es float ge=0, DB puede ser int
            "calc": calc_db_map.get(input_payload.CALC, -1),
            
            "mtrans": input_payload.MTRANS, # Asumiendo que es TEXT en Supabase
            
            "nobeyesdad": nobeyesdad_value, 
            "bmi": prediction_data.bmi, # Asumiendo que es double precision en Supabase
            "created_at": pd.Timestamp.now(tz='UTC').isoformat()
        }
        
        logging.info(f"Preparando inserción en Supabase (tabla '{settings.SUPABASE_TABLE_NAME}'). Payload FINAL: {data_to_insert}")
        print(f"DEBUG (server/db_service): Payload FINAL enviado a Supabase: {data_to_insert}") # Para máxima visibilidad

        response = await supabase_client_instance.table(settings.SUPABASE_TABLE_NAME).insert(data_to_insert).execute()
        
        if hasattr(response, 'data') and response.data:
            logging.info(f"Predicción guardada en Supabase. Registros insertados: {len(response.data)}")
        else:
            # A veces Supabase devuelve una lista vacía en 'data' para inserciones exitosas si no hay 'returning'
            logging.info(f"Guardado en Supabase completado (o sin error de API). Respuesta: {response}")

    except Exception as e:
        logging.error(f"Error CRÍTICO al guardar predicción en Supabase: {e}")
        logging.exception("Detalles del error al guardar en Supabase (save_prediction_to_db):")