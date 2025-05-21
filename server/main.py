from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI()

class ObesityInput(BaseModel):
    gender: Literal["Male", "Female"]
    age: float
    height: float
    weight: float
    bmi: float
    family_history_with_overweight: Literal["yes", "no"]
    FAVC: Literal["yes", "no"]
    FCVC: float
    NCP: float
    CAEC: Literal["no", "Sometimes", "Frequently", "Always"]
    CH2O: float
    SCC: Literal["yes", "no"]
    FAF: float
    TUE: float
    CALC: Literal["no", "Sometimes", "Frequently", "Always"]

@app.get("/")
def root():
    return {"message": "FastAPI is working"}

@app.post("/predict")
def predict_obesity(input: ObesityInput):
    # ⚠️ Simulación temporal
    bmi = input.bmi
    if bmi < 18.5:
        level = "Underweight"
    elif bmi < 25:
        level = "Normal Weight"
    elif bmi < 30:
        level = "Overweight"
    elif bmi < 35:
        level = "Obesity Level 1"
    elif bmi < 40:
        level = "Obesity Level 2"
    else:
        level = "Obesity Level 3"

    return {"prediction": level}
