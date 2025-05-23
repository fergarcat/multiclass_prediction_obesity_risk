import pandas as pd
from client.services.db import engine

def get_field_data():
    query = "SELECT id, label, data_type FROM public.app_features WHERE active = TRUE AND label NOT IN ('NObeyesdad') ORDER BY id;"
    df = pd.read_sql(query, engine)

    return {
        row['id']: {
            "id": row['id'],
            "label": row['label'],
            "type": (
                "select" if (
                    row['data_type'] == 'boolean' or
                    (row['data_type'] == 'text' and row['label'].lower() in ['gender', 'calc', 'caec'])
                ) else "number"
            ),
            "options": (
                ['yes', 'no'] if row['data_type'] == 'boolean'
                else ['Male', 'Female'] if row['label'].lower() == 'gender'
                else ['Always', 'Frequently', 'Sometimes', 'no'] if row['label'].lower() in ['calc', 'caec']
                else []
            )
        }
        for _, row in df.iterrows()
    }
