from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Document, DocumentChunk
from app.schemas.document import DocumentRead, DocumentChunkRead

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/", response_model=List[DocumentRead])
def list_documents(project_id: UUID = None, db: Session = Depends(get_db)):
    """List all uploaded project documents."""
    query = db.query(Document)
    if project_id:
        query = query.filter(Document.project_id == project_id)
    return query.all()


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(document_id: UUID, db: Session = Depends(get_db)):
    """Retrieve document metadata and status."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.get("/{document_id}/chunks", response_model=List[DocumentChunkRead])
def get_document_chunks(document_id: UUID, db: Session = Depends(get_db)):
    """Retrieve text chunks for a document."""
    chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).order_by(DocumentChunk.chunk_index).all()
    return chunks
