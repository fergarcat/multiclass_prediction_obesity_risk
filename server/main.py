from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle
import os

app = FastAPI()

# CORS: permitir peticiones desde la app Dash
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringirlo a "http://localhost:8050" si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el modelo
model_path = os.path.join(os.path.dirname(__file__), "obesity_model.pkl")
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"❌ Error cargando el modelo: {e}")

@app.get("/")
def read_root():
    return {"message": "FastAPI is working"}

@app.post("/predict")
def predict(data: dict):
    try:
        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
