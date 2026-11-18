from pathlib import Path
from typing import List, Dict, Any
import pymupdf
from pydantic import BaseModel, Field
from papertrail.ingestion.utils import get_file_metadata

class PageDocument(BaseModel):
    page_number: int = Field(..., description="1-indexed page number")
    content: str = Field(..., description="Extracted raw text content of the page")

class ParsedPDFResult(BaseModel):
    filename: str
    sha256: str
    size_bytes: int
    page_count: int
    title: str
    pages: List[PageDocument]

class PyMuPDFParser:
    """Modular PyMuPDF parser for PaperTrail ingestion pipeline."""
    
    @staticmethod
    def parse(pdf_path: str | Path) -> ParsedPDFResult:
        """
        Parses a PDF file, extracts file-level metadata (sha256, size), 
        and extracts page-by-page text content.
        """
        path = Path(pdf_path)
        
        # 1. Get file-level metadata using our utils module
        file_meta = get_file_metadata(path)

        # 2. Open PDF with pymupdf
        doc = pymupdf.open(path)
        parsed_pages: List[PageDocument] = []

        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            parsed_pages.append(
                PageDocument(
                    page_number=page_num + 1,
                    content=text
                )
            )

        # 3. Form a baseline title from the filename (to satisfy the database model requirements)
        default_title = path.stem.replace("_", " ").title()

        return ParsedPDFResult(
            filename=file_meta["filename"],
            sha256=file_meta["sha256"],
            size_bytes=file_meta["size_bytes"],
            page_count=len(doc),
            title=default_title,
            pages=parsed_pages
        )

if __name__ == "__main__":
    sample_pdf = Path("data/raw/sample.pdf")
    if sample_pdf.exists():
        print(f"Parsing {sample_pdf.name} with metadata...")
        result = PyMuPDFParser.parse(sample_pdf)
        print(f"Filename: {result.filename}")
        print(f"SHA256: {result.sha256}")
        print(f"Size (bytes): {result.size_bytes}")
        print(f"Page Count: {result.page_count}")
        print(f"Title: {result.title}")
    else:
        print(f"Sample PDF not found at {sample_pdf}.")