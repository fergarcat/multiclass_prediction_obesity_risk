import pandas as pd
from sqlalchemy import text
from client.services.db import engine

def get_field_data():
    query = 'SELECT * FROM public.app_features LIMIT 1;'
    df = pd.read_sql(query, engine)
    return df.columns.tolist()

def insert_user_input(data_dict):
    columns = ', '.join(data_dict.keys())
    values = ', '.join([f":{k}" for k in data_dict.keys()])
    query = text(f'INSERT INTO public.obesity_risk ({columns}) VALUES ({values});')
    
    with engine.begin() as conn:
        conn.execute(query, **data_dict)
