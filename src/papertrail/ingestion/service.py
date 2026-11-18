import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from papertrail.db.models import Document, DocumentStatus
from papertrail.ingestion.parser import PyMuPDFParser

def store_document_metadata(db: Session, tenant_id: uuid.UUID, pdf_path: str | Path) -> Document:
    """
    Parses a PDF file and securely stores or retrieves its metadata record 
    in PostgreSQL, maintaining idempotency via sha256 hash.
    """
    # 1. Parse the PDF to extract metadata and file details
    parsed_result = PyMuPDFParser.parse(pdf_path)

    # 2. Check if this document already exists for this tenant (Idempotency)
    existing_doc = db.query(Document).filter_by(
        tenant_id=tenant_id, 
        sha256=parsed_result.sha256
    ).first()

    if existing_doc:
        print(f"Document already exists in DB (ID: {existing_doc.id})")
        return existing_doc

    # 3. Create a new Document record matching models.py
    new_doc = Document(
        tenant_id=tenant_id,
        filename=parsed_result.filename,
        sha256=parsed_result.sha256,
        size_bytes=parsed_result.size_bytes,
        status=DocumentStatus.PROCESSING,
        page_count=parsed_result.page_count,
        title=parsed_result.title,
        year=None,
        authors=["Unknown"],
    )

    # 4. Commit to database
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    print(f"Successfully stored metadata for new document ID: {new_doc.id}")
    return new_doc