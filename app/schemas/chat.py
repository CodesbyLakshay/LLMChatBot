from pydantic import BaseModel
from datetime import datetime


class UploadResponse(BaseModel):
    message: str
    document_id: int
    file_name: str

class ChatRequest(BaseModel):
    question: str
    document_id: int

class ChatResponse(BaseModel):
    answer: str

class DocumentResponse(BaseModel):
    id: int
    file_name: str
    uploaded_At: datetime

    class Config:
        from_attributes = True
