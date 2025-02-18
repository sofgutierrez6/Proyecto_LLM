# app/api/documents.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.document import Document
from app.schemas.document import Document as DocumentSchema, DocumentCreate
from app.services.document_processor import DocumentProcessor
from app.services.llm_service import LLMService

router = APIRouter()

@router.post("/upload", response_model=DocumentSchema)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    content, file_path = await DocumentProcessor.process_document(file)
    
    document = Document(
        title=file.filename,
        content=content,
        file_path=file_path,
        owner_id=current_user_id
    )
    
