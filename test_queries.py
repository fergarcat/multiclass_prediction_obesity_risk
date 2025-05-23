from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

USER = "postgres.pfhjkvnfjfpgxhwoupwz"
PASSWORD = "R@RydQxyik5A7a)"
HOST = "aws-0-eu-west-2.pooler.supabase.com"
PORT = "6543"
DBNAME = "postgres"

PASSWORD_ENCODED = quote_plus(PASSWORD)
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD_ENCODED}@{HOST}:{PORT}/{DBNAME}?sslmode=prefer"

engine = create_engine(DATABASE_URL)

def run_queries():
    try:
        with engine.connect() as connection:
            # Crear tabla de prueba
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INT
                )
            """))
            print("Tabla creada o ya existente")

            # INSERTAR datos
            connection.execute(text("""
                INSERT INTO test_table (name, age) VALUES
                ('Alice', 30),
                ('Bob', 25)
            """))
            print("Datos insertados")

            # SELECT datos
            result = connection.execute(text("SELECT * FROM test_table"))
            print("Datos en test_table:")
            for row in result:
                print(row)

            # UPDATE datos
            connection.execute(text("""
                UPDATE test_table SET age = age + 1 WHERE name = 'Alice'
            """))
            print("Datos actualizados")

            # SELECT para ver actualización
            result = connection.execute(text("SELECT * FROM test_table WHERE name = 'Alice'"))
            print("Datos actualizados para Alice:")
            for row in result:
                print(row)

            # DELETE datos
            connection.execute(text("""
                DELETE FROM test_table WHERE name = 'Bob'
            """))
            print("Datos eliminados")

            # SELECT final para ver estado
            result = connection.execute(text("SELECT * FROM test_table"))
            print("Estado final de test_table:")
            for row in result:
                print(row)

    except Exception as e:
        print("Error en las consultas:", e)

if __name__ == "__main__":
    run_queries()
