from sqlalchemy import text
from server.core.config import settings
from sqlalchemy import create_engine

engine = create_engine(settings.DATABASE_URL)

# Mapas de conversión
gender_map = {"Male": 1, "Female": 0}
binary_map = {"yes": 1, "no": 0}
caec_map = {"Always": 3, "Frequently": 2, "Sometimes": 1, "no": 0}
calc_map = {"Always": 3, "Frequently": 2, "Sometimes": 1, "no": 0}
nobeyesdad_map = {
    "Insufficient_Weight": 0,
    "Normal_Weight": 1,
    "Overweight_Level_I": 2,
    "Overweight_Level_II": 3,
    "Obesity_Type_I": 4,
    "Obesity_Type_II": 5,
    "Obesity_Type_III": 6
}

def insert_obesity_record(data: dict):
    processed = {
        "gender": gender_map.get(data.get("gender"), 0),
        "age": int(data.get("age", 0)),
        "fhwo": binary_map.get(data.get("family_history_with_overweight"), 0),
        "favc": binary_map.get(data.get("favc"), 0),
        "fcvc": int(data.get("fcvc", 0)),
        "ncp": int(data.get("ncp", 0)),
        "caec": caec_map.get(data.get("caec"), 0),
        "ch2o": int(data.get("ch2o", 0)),
        "scc": binary_map.get(data.get("scc"), 0),
        "faf": int(data.get("faf", 0)),
        "tue": int(data.get("tue", 0)),
        "calc": calc_map.get(data.get("calc"), 0),
        "nobeyesdad": nobeyesdad_map.get(data.get("nobeyesdad"), 0),
        "bmi": float(data.get("bmi", 0))
    }

    insert_query = """
        INSERT INTO fe_obesity_risk_classification (
            gender, age, family_history_with_overweight, favc, fcvc, ncp, caec,
            ch2o, scc, faf, tue, calc, nobeyesdad, bmi, created_at
        ) VALUES (
            :gender, :age, :fhwo, :favc, :fcvc, :ncp, :caec,
            :ch2o, :scc, :faf, :tue, :calc, :nobeyesdad, :bmi, NOW()
        )
    """

    with engine.connect() as conn:
        conn.execute(text(insert_query), processed)
        conn.commit()