from sqlalchemy import create_engine
from urllib.parse import quote_plus

USER = "postgres.pfhjkvnfjfpgxhwoupwz"
PASSWORD = "R@RydQxyik5A7a)"
HOST = "aws-0-eu-west-2.pooler.supabase.com"
PORT = "6543"
DBNAME = "postgres"

# Codificamos la contraseña para que los caracteres especiales no rompan la URL
PASSWORD_ENCODED = quote_plus(PASSWORD)

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD_ENCODED}@{HOST}:{PORT}/{DBNAME}?sslmode=prefer"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Conexión exitosa!")
except Exception as e:
    print("Error al conectar:", e)
