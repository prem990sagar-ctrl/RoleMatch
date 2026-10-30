"""
Module: utils/pdf_extractor.py
Purpose: Backward-compatible adapter delegating to models.pdf_model.PDFModel.
"""
from models.pdf_model import (
    PDFModel,
    PDFProcessingError,
    FileSizeExceededError,
    EncryptedPDFError,
    EmptyPDFError,
    MAX_FILE_SIZE_BYTES
)


def extract_text_from_pdf(pdf_source, max_size_bytes: int = MAX_FILE_SIZE_BYTES) -> str:
    """Extract text from PDF source delegating to the MVC PDFModel."""
    return PDFModel.extract_text(pdf_source, max_size_bytes=max_size_bytes)
