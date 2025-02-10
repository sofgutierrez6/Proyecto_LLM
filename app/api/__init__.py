# api/__init__.py
from fastapi import APIRouter
from .users import router as users_router
from .documents import router as documents_router
from .auth import router as auth_router
