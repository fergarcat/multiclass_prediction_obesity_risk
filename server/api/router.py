from fastapi import APIRouter, HTTPException, Body, Depends
from ..model.prediction_model import (
    PredictionInput, PredictionOutput, Message, HealthCheckResponse
)
from ..services.prediction_service import make_prediction
from ..services.model_loader import are_models_loaded_successfully
# from ..services.db_service import get_supabase_client, save_prediction_to_db # Para después
# from supabase_async_client import AsyncClient # Para después

router = APIRouter()

# Health check (ya lo tienes y debería funcionar con la carga real)
@router.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check_endpoint():
    models_ready = are_models_loaded_successfully()
    if not models_ready:
        raise HTTPException(status_code=503, detail="Modelos de ML no cargados o no listos.")
    return HealthCheckResponse(status="ok", message="Servicio operativo y modelos cargados.", models_loaded=True)

# NUEVO ENDPOINT DE PREDICCIÓN
@router.post(
    "/predict",
    response_model=PredictionOutput,
    summary="Realiza una predicción del riesgo de obesidad",
    tags=["Predictions"],
    responses={
        400: {"model": Message, "description": "Datos de entrada inválidos o error de procesamiento"},
        422: {"model": Message, "description": "Error de validación de entrada (FastAPI)"},
        500: {"model": Message, "description": "Error interno del servidor"},
        503: {"model": Message, "description": "Servicio no disponible (modelos no cargados)"},
    }
)
async def predict_obesity_risk(
    input_data: PredictionInput = Body(..., examples=PredictionInput.model_config["json_schema_extra"]["examples"]),
    # supabase: AsyncClient = Depends(get_supabase_client) # Para después
):
    if not are_models_loaded_successfully():
        raise HTTPException(status_code=503, detail="Modelos de ML no están cargados o no están listos.")

    try:
        # make_prediction ahora devuelve (categoría_string, índice_para_db)
        predicted_category_string, predicted_index_for_db = await make_prediction(input_data)

        # TODO: Aquí iría la lógica para guardar en Supabase usando predicted_index_for_db
        # if supabase and predicted_index_for_db is not None:
        #     try:
        #         await save_prediction_to_db(
        #             client=supabase,
        #             input_payload=input_data.model_dump(by_alias=True),
        #             prediction_index=predicted_index_for_db # Enviar índice numérico
        #         )
        #     except Exception as db_e:
        #         print(f"WARN: No se pudo guardar en Supabase: {db_e}")
        # else:
        #      print(f"DEBUG: Supabase no configurado o índice de predicción nulo ({predicted_index_for_db}). No se guarda.")


        return PredictionOutput(obesity_risk_category=predicted_category_string)

    except ValueError as ve: # Errores de procesamiento de predicción
        raise HTTPException(status_code=400, detail=f"Error en datos o procesamiento: {str(ve)}")
    except RuntimeError as rte: # Si los modelos fallan internamente
        raise HTTPException(status_code=503, detail=str(rte))
    except Exception as e:
        import traceback
        print(f"ERROR: Excepción inesperada en /predict: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Ocurrió un error interno del servidor.")
