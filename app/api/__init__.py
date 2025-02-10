# api/__init__.py
from fastapi import APIRouter
from .users import router as users_router
from .documents import router as documents_router
from .auth import router as auth_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(documents_router, prefix="/documents", tags=["documents"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
