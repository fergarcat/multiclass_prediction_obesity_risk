from ..model.prediction_model import PredictionRequest, PredictionResponse
from ..services.model_loader import get_obesity_model_instance
import logging

class PredictionService:
    """Servicio que coordina la predicción del modelo y el guardado en base de datos."""

    def __init__(self):
        self.obesity_model = None  # Se inicializa con lazy loading

    async def make_prediction(self, data: PredictionRequest) -> PredictionResponse:
        try:
            self.obesity_model = get_obesity_model_instance()

            prediction_result: PredictionResponse = self.obesity_model.predict(data)
            logging.info(f"✅ Predicción realizada: {prediction_result.prediction} (BMI: {prediction_result.bmi})")

            # Import diferido para evitar inicialización temprana
            from ..services.db_service import save_prediction_to_db
            await save_prediction_to_db(prediction_result)
            logging.info("✅ Predicción enviada para guardar en Supabase.")

            return prediction_result
        except RuntimeError as e:
            logging.error(f"🚫 Servicio no disponible: {e}")
            raise
        except Exception as e:
            logging.error(f"❌ Error en el servicio de predicción: {e}")
            logging.exception("Detalles del error en make_prediction:")
            raise

# Instancia global para inyección de dependencias
prediction_service_instance = PredictionService()
