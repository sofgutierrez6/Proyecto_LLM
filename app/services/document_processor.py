# app/services/document_processor.py
import os
from typing import Optional
import aiohttp
from fastapi import UploadFile
import PyPDF2
import docx
import markdown

class DocumentProcessor:
    @staticmethod
    async def process_document(file: UploadFile) -> tuple[str, str]:
        content = ""
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        if file.filename.endswith('.pdf'):
            content = DocumentProcessor._process_pdf(file_path)
        elif file.filename.endswith('.docx'):
            content = DocumentProcessor._process_docx(file_path)
        elif file.filename.endswith('.md'):
            content = DocumentProcessor._process_markdown(file_path)
        elif file.filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
        return content, file_path

    @staticmethod
    def _process_pdf(file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    @staticmethod
    def _process_docx(file_path: str) -> str:
        doc = docx.Document(file_path)
        return " ".join([paragraph.text for paragraph in doc.paragraphs])

    @staticmethod
    def _process_markdown(file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return markdown.markdown(file.read())
