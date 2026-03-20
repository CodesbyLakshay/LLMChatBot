import logging

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.utils import get_current_user
from app.database import get_async_session
from app.services.text_extractor import extract_text_from_file , save_upload_to_disk , validate_file_extension
from app.services.ai_groq import ask_groq
from app.models.user import User
from app.models.document import Document
from app.schemas.chat import UploadResponse, ChatRequest, ChatResponse, DocumentResponse


router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...),current_user: User = Depends(get_current_user),db: AsyncSession = Depends(get_async_session)
):
    validate_file_extension(file.filename)
    file_path = await save_upload_to_disk(file)

    try:
        extracted_text = extract_text_from_file(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not read file: {str(e)}")

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="The file appears to be empty or has no readable text.")

    document = Document(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_path,
        extracted_text=extracted_text
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    return UploadResponse(
        message="File uploaded and processed. You can now ask questions about it.",
        document_id=document.id,
        file_name=file.filename
    )


@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest, current_user: User = Depends(get_current_user),db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(
        select(Document).where(Document.id == request.document_id)
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have access to this document")

    logger.info(request.question , document.extracted_text)
    try:
        answer = await ask_groq(question=request.question, document_text=document.extracted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting answer from AI: {str(e)}")

    return ChatResponse(
        answer=answer
    )


@router.get("/documents", response_model=List[DocumentResponse])
async def list_documents(current_user: User = Depends(get_current_user),db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(
        select(Document).where(Document.user_id == current_user.id)
    )
    documents = result.scalars().all()
    return documents
