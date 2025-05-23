from fastapi import APIRouter, Request
from client.services.db import insert_obesity_record
from pydantic import BaseModel
from server.services.prediction_service import make_prediction_with_advice

router = APIRouter()

class PredictionInput(BaseModel):
    data: dict

@router.post("/predict")
async def predict(request: Request):
    data = await request.json()
    print("INPUT DATA:", data)  # debug
    result = await make_prediction_with_advice(data)
    return result

@router.post("/submit-obesity-data")
async def submit_obesity_data(request: Request):
    data = await request.json()
    insert_obesity_record(data)
    return {"status": "success", "message": "Datos guardados correctamente"}