import os

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DB_CONFIG = {
    "server": "YOUR_SERVER",
    "database": "YOUR_DB",
    "username": "USER",
    "password": "PASS",
    "driver": "ODBC Driver 17 for SQL Server"
}