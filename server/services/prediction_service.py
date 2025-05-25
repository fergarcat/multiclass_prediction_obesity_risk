# server/services/prediction_service.py
from ..model.prediction_model import PredictionRequest, PredictionResponse
from ..services.model_loader import get_obesity_model_instance
from ..services.db_service import save_prediction_to_db # Importa la función de guardado
import logging

class PredictionService:
    """Servicio que coordina la predicción del modelo y el guardado en base de datos."""

    def __init__(self):
        self.obesity_model = None # Se inicializa al llamar a get_obesity_model_instance

    async def make_prediction(self, data: PredictionRequest) -> PredictionResponse:
        try:
            # Obtiene la instancia del modelo de ML. Esto fallará si los modelos no cargaron.
            self.obesity_model = get_obesity_model_instance()

            # Realiza la predicción usando la instancia del modelo
            prediction_result: PredictionResponse = self.obesity_model.predict(data)
            logging.info(f"Predicción realizada: {prediction_result.prediction} (BMI: {prediction_result.bmi})")

            # Intenta guardar la predicción en la base de datos
            # Esta operación es async, así que la 'await'.
            await save_prediction_to_db(prediction_result)
            logging.info("Predicción enviada para ser guardada en Supabase.")

            return prediction_result
        except RuntimeError as e: # Captura errores si el modelo no está cargado
            logging.error(f"Servicio no disponible: {e}")
            raise # Relanza para que FastAPI devuelva un 503
        except Exception as e:
            logging.error(f"Error en el servicio de predicción: {e}")
            logging.exception("Detalles del error en make_prediction:") # Imprime el stack trace
            raise # Relanza para que FastAPI devuelva un 500

# Crea una instancia global del servicio de predicción para inyección de dependencias
prediction_service_instance = PredictionService()