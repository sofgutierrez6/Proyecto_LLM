# api/documents.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from models.document import Document
from schemas.document import DocumentCreate, DocumentInDB
from services.document_processor import DocumentProcessor
from services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

@router.post("/documents/", response_model=DocumentInDB)
async def create_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Process document based on file type
    content = ""
    if file.content_type == "application/pdf":
        content = await DocumentProcessor.process_pdf(file.file)
    elif file.content_type == "text/plain":
        content = await DocumentProcessor.process_text(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Generate summary using LLM
    summary = await llm_service.generate_summary(content)
    
    # Create document in database
    db_document = Document(
        title=file.filename,
        content=content,
        summary=summary,
        file_path=f"uploads/{file.filename}"
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@router.get("/documents/{document_id}/qa")
async def answer_question(
    document_id: int,
    question: str,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    answer = await llm_service.answer_question(document.content, question)
    return {"answer": answer}
