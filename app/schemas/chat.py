from pydantic import BaseModel
from datetime import datetime


class UploadResponse(BaseModel):
    message: str
    document_id: int
    filename: str

class ChatRequest(BaseModel):
    question: str
    document_id: int

class ChatResponse(BaseModel):
    answer: str

class DocumentResponse(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
