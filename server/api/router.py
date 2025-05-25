# server/api/router.py
from fastapi import APIRouter, HTTPException, Body, Depends, status
from ..model.prediction_model import PredictionRequest, PredictionResponse
from ..core.schemas import Message, HealthCheckResponse
from ..services.prediction_service import prediction_service_instance
from ..services.model_loader import are_models_loaded_successfully
import logging

router = APIRouter()

# Health check
@router.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check_endpoint():
    models_ready = are_models_loaded_successfully()
    if not models_ready:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Modelos de ML no cargados o no listos.")
    return HealthCheckResponse(status="ok", message="Servicio operativo y modelos cargados.", models_loaded=True)

# Endpoint de predicción
@router.post(
    "/prediction", # Cambiado de /predict a /prediction para ser consistente con el frontend
    response_model=PredictionResponse,
    summary="Realiza una predicción del riesgo de obesidad y la guarda en DB",
    tags=["Predictions"],
    status_code=status.HTTP_200_OK, # Por defecto es 200 si la respuesta_model coincide
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Message, "description": "Datos de entrada inválidos o error de procesamiento"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Message, "description": "Error de validación de entrada (FastAPI)"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message, "description": "Error interno del servidor"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": Message, "description": "Servicio no disponible (modelos no cargados)"},
    }
)
async def predict_obesity_risk(
    request_data: PredictionRequest = Body(...), # Usamos PredictionRequest aquí
):
    # La comprobación de modelos cargados se hará dentro del prediction_service, que lanza RuntimeError
    # si no están listos, y eso es capturado y mapeado a 503 por el try/except del endpoint.
    try:
        # Llamamos a la instancia del servicio para hacer la predicción y el guardado
        response = await prediction_service_instance.make_prediction(request_data)
        return response

    except RuntimeError as e: # Error si los modelos no están cargados
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except ValueError as ve: # Errores específicos del servicio
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error en datos o procesamiento: {str(ve)}")
    except Exception as e: # Cualquier otro error inesperado
        logging.error(f"ERROR: Excepción inesperada en /prediction: {e}", exc_info=True) # exc_info=True para el traceback
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrió un error interno del servidor.")