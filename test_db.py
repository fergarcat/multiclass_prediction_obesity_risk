import os
from sqlalchemy import create_engine, text

db_url = os.getenv("DATABASE_URL")
print("DATABASE_URL:", db_url)

engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Conexión exitosa:", result.fetchone())
except Exception as e:
    print("Error conectando a la base de datos:", e)
