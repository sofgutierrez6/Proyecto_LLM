# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api_router  # Importa el router principal
from core.config import settings
import psycopg2

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye el router principal
app.include_router(api_router, prefix=settings.API_V1_STR)

try:
    connection = psycopg2.connect(
        user="tu_usuario",
        password="tu_contraseña",
        host="127.0.0.1",
        port="5432",
        database="tu_base_de_datos"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Conectado a - ", record, "\n")
except (Exception, psycopg2.Error) as error:
    print("Error al conectar a PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Conexión a PostgreSQL cerrada")
