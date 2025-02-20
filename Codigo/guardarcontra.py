from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

print(f"Usuario: {DB_USER}")