from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    content: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentInDB(DocumentBase):
    id: int
    file_path: str
    summary: Optional[str]
    created_at: datetime
    owner_id: int
    
    class Config:
        from_attributes = True
