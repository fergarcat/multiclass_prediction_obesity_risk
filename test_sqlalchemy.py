from sqlalchemy import create_engine
import os

# Variables directamente, para no depender de .env por ahora
USER = "postgres.pfhjkvnfjfpgxhwoupwz"
PASSWORD = "R@RydQxyik5A7a)"
HOST = "aws-0-eu-west-2.pooler.supabase.com"
PORT = "6543"
DBNAME = "postgres"

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Conexión SQLAlchemy exitosa")
except Exception as e:
    print("Error al conectar:", e)
