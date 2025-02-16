# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api_router  # Importa el router principal
from core.config import settings

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
