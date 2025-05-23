import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres.pfhjkvnfjfpgxhwoupwz",
        password="R@RydQxyik5A7a)",
        host="aws-0-eu-west-2.pooler.supabase.com",
        port="6543",
        sslmode="require"
    )
    print("Conexión directa exitosa!")
    conn.close()
except Exception as e:
    print("Error en conexión directa:", e)
