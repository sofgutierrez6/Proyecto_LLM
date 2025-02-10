# db/__init__.py
from .session import SessionLocal, engine, get_db
from .base import Base

# Make sure all models are imported
from models.user import User
from models.document import Document

# Initialize models
Base.metadata.create_all(bind=engine)
