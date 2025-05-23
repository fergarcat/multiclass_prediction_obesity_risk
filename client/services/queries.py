from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from client.config.fields_config import get_field_data

# --- Configuración conexión a la base de datos ---
USER = "postgres.pfhjkvnfjfpgxhwoupwz"
PASSWORD = "R@RydQxyik5A7a)"  # pon tu password real aquí
HOST = "aws-0-eu-west-2.pooler.supabase.com"
PORT = "6543"
DBNAME = "postgres"

PASSWORD_ENCODED = quote_plus(PASSWORD)
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD_ENCODED}@{HOST}:{PORT}/{DBNAME}?sslmode=prefer"

engine = create_engine(DATABASE_URL)
# -----------------------------------------------

def insert_user_input(data_dict):
    fields = get_field_data()
    data_named = {}

    for key, value in data_dict.items():
        if key in fields:
            col_name = fields[key]['label']
            data_named[col_name] = value
        else:
            raise KeyError(f"Campo desconocido con id {key}")

    columns = ', '.join(data_named.keys())
    placeholders = ', '.join([f":{col}" for col in data_named.keys()])
    query = f"INSERT INTO public.fe_obesity_risk_classification ({columns}) VALUES ({placeholders})"

    with engine.connect() as conn:
        conn.execute(text(query), data_named)
        conn.commit()

def get_prediction_advice(prediction_class: str):
    query = """
        SELECT h.header, t.text 
        FROM tip_header h
        JOIN tip_text t ON h.id = t.header_id
        WHERE h.class = :prediction_class
    """
    with engine.connect() as conn:
        result = conn.execute(text(query), {"prediction_class": prediction_class})
        row = result.fetchone()
        return {
            "header": row["header"] if row else "",
            "text": row["text"] if row else ""
        }