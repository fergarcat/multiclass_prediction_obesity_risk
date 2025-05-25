# server/api/router.py

from fastapi import APIRouter, HTTPException, Body, status
from ..model.prediction_model import PredictionRequest, PredictionResponse
from ..core.schemas import Message, HealthCheckResponse
from ..services.prediction_service import prediction_service_instance
from ..services.model_loader import are_models_loaded_successfully
from ..services.supabase_client import get_supabase_client
import logging

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check_endpoint():
    models_ready = are_models_loaded_successfully()
    if not models_ready:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Modelos de ML no cargados o no listos.")
    return HealthCheckResponse(status="ok", message="Servicio operativo y modelos cargados.", models_loaded=True)

@router.post(
    "/prediction",
    response_model=PredictionResponse,
    summary="Realiza una predicción del riesgo de obesidad y la guarda en DB",
    tags=["Predictions"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Message, "description": "Datos de entrada inválidos o error de procesamiento"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Message, "description": "Error de validación de entrada (FastAPI)"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message, "description": "Error interno del servidor"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": Message, "description": "Servicio no disponible (modelos no cargados o Supabase no disponible)"},
    }
)
async def predict_obesity_risk(
    request_data: PredictionRequest = Body(...),
):
    try:
        # Verifica que Supabase esté listo antes de intentar usarlo
        _ = get_supabase_client()
        logging.info("✅ Supabase client está inicializado correctamente.")

        # Realiza la predicción
        response = await prediction_service_instance.make_prediction(request_data)
        return response

    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error en datos o procesamiento: {str(ve)}")
    except Exception as e:
        logging.error(f"ERROR: Excepción inesperada en /prediction: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrió un error interno del servidor.")
