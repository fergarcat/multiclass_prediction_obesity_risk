# test_env_vars.py
import os
from dotenv import load_dotenv

load_dotenv()  # carga variables desde .env

def main():
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port")
    dbname = os.getenv("dbname")

    # Quitamos espacios extra si hay
    user = user.strip() if user else None
    password = password.strip() if password else None
    host = host.strip() if host else None
    port = port.strip() if port else None
    dbname = dbname.strip() if dbname else None

    print(f"user='{user}'")
    print(f"password='{password}'")
    print(f"host='{host}'")
    print(f"port='{port}'")
    print(f"dbname='{dbname}'")

if __name__ == "__main__":
    main()
