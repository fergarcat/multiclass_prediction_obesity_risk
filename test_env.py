from dotenv import load_dotenv
import os

load_dotenv()

for key in ["user", "password", "host", "port", "dbname"]:
    value = os.getenv(key)
    print(f"{key} = {value} (type: {type(value)})")
