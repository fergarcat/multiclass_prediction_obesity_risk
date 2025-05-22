from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

# --- Enums (copia y adapta de nuestra discusión anterior) ---
class GenderEnum(str, Enum): male = "Male"; female = "Female"
class YesNoEnum(str, Enum): yes = "yes"; no = "no"
# ... (define todos los Enums que necesites para CALC, CAEC, MTRANS, etc.)
# Asegúrate que los valores de los enums coincidan con lo que enviará el frontend

class PredictionInput(BaseModel):
    # Aquí van todas tus features como se describen en tu tabla app_features
    # y como las espera tu pipeline de preprocesamiento.
    # EJEMPLO (¡DEBES COMPLETARLO CON TUS FEATURES EXACTAS!):
    Gender: GenderEnum
    Age: float = Field(..., gt=0, le=120, description="Edad en años")
    Height: float = Field(..., gt=0.5, le=2.5, description="Altura en metros")
    Weight: float = Field(..., gt=10, le=300, description="Peso en kilogramos")
    family_history_with_overweight: YesNoEnum
    FAVC: YesNoEnum
    FCVC: float = Field(..., ge=1, le=3)
    NCP: float = Field(..., ge=1, le=4)
    # CAEC: CAECEnum
    SMOKE: YesNoEnum
    CH2O: float = Field(..., ge=1, le=3)
    SCC: YesNoEnum
    FAF: float = Field(..., ge=0, le=3)
    TUE: float = Field(..., ge=0, le=2)
    # CALC: CALCEnum
    # MTRANS: MTRANSEnum

    # Configuración para ejemplos en Swagger (Pydantic v2+)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Gender": "Female", "Age": 21.0, "Height": 1.62, "Weight": 64.0,
                    "family_history_with_overweight": "yes", "FAVC": "no", "FCVC": 2.0, "NCP": 3.0,
                    # "CAEC": "Sometimes", # Ejemplo para Enum
                    "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 0.0, "TUE": 1.0,
                    # "CALC": "no", # Ejemplo para Enum
                    # "MTRANS": "Public_Transportation" # Ejemplo para Enum
                    # ¡COMPLETA EL EJEMPLO CON TODAS TUS FEATURES!
                }
            ]
        }
    }

class PredictionOutput(BaseModel):
    obesity_risk_category: str = Field(..., description="Categoría de riesgo de obesidad predicha")
    # Opcional: si tu modelo devuelve probabilidades
    # class_probabilities: Optional[dict[str, float]] = None

class Message(BaseModel): # Para respuestas de error genéricas
    detail: str

# HealthCheckResponse ya está definida y está bien por ahora.
# from pydantic import BaseModel
# from typing import Any, Optional (ya importados arriba)
class HealthCheckResponse(BaseModel):
    status: str
    message: Optional[str] = None
    models_loaded: Optional[bool] = None