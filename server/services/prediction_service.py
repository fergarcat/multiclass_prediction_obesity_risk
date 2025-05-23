import os
import joblib
import numpy as np
from server.services.db_service import get_advice_for_prediction, insert_user_input
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(ROOT_DIR, "data", "modeling", "pkl", "xgboost_optuna_pipeline.pkl")

model = joblib.load(MODEL_PATH)

def make_prediction_with_advice(input_data: dict):
    try:
        insert_user_input(input_data)
    except Exception as e:
        print(f"ERROR: No se pudieron guardar los datos del usuario: {e}")

    input_array = np.array([list(input_data.values())])
    prediction = model.predict(input_array)[0]
    advice = get_advice_for_prediction(prediction)

    return {
        "prediction": prediction,
        "header": advice["header"],
        "text": advice["text"],
        "label": prediction  # útil para graficar
    }
