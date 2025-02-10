# services/document_processor.py
from typing import Optional
import PyPDF2
from io import BytesIO

class DocumentProcessor:
    @staticmethod
    async def process_pdf(file: BytesIO) -> str:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    @staticmethod
    async def process_text(file: BytesIO) -> str:
        return file.read().decode('utf-8')
