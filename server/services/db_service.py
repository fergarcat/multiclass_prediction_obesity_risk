import psycopg2
import os
from sqlalchemy import create_engine, text
from server.core.config import settings

engine = create_engine(settings.DATABASE_URL)

def get_advice_for_prediction(prediction_class: str):
    query = """
        SELECT h.header, t.text 
        FROM tip_header h
        JOIN tip_text t ON h.id = t.header_id
        WHERE h.class = :cls
        LIMIT 1;
    """
    with engine.connect() as conn:
        result = conn.execute(text(query), {"cls": prediction_class})
        row = result.fetchone()
        return {
            "header": row["header"] if row else "",
            "text": row["text"] if row else ""
        }

def insert_user_input(data_dict: dict):
    # Opcionalmente puedes mapear los nombres a los nombres reales de columnas si difieren
    columns = ', '.join(data_dict.keys())
    placeholders = ', '.join([f":{col}" for col in data_dict.keys()])
    query = f"INSERT INTO public.fe_obesity_risk_classification ({columns}) VALUES ({placeholders})"

    with engine.connect() as conn:
        conn.execute(text(query), data_dict)
        conn.commit()