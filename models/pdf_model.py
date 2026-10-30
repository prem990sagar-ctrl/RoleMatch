"""
Module: models/pdf_model.py
Purpose: PDF parsing, validation, and plain-text extraction model using PyPDF.
"""
import io
import os
from typing import Union
from pypdf import PdfReader
from pypdf.errors import PdfReadError

# Limit resume uploads to 10 MB
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


class PDFProcessingError(Exception):
    """Base exception for PDF parsing and validation errors."""
    pass


class FileSizeExceededError(PDFProcessingError):
    """Raised when file size exceeds maximum allowed threshold."""
    pass


class EncryptedPDFError(PDFProcessingError):
    """Raised when the document is password-protected or encrypted."""
    pass


class EmptyPDFError(PDFProcessingError):
    """Raised when no extractable text is found (e.g. scanned/image-only document)."""
    pass


class PDFModel:
    """Model responsible for validating and parsing PDF documents."""

    @staticmethod
    def extract_text(pdf_source: Union[str, bytes, io.BytesIO], max_size_bytes: int = MAX_FILE_SIZE_BYTES) -> str:
        """
        Extract readable plain text from a PDF source stream, file path, or bytes.

        Args:
            pdf_source: Path to file, raw bytes, or BytesIO buffer.
            max_size_bytes: Maximum size allowed in bytes.

        Returns:
            Extracted text string.

        Raises:
            FileSizeExceededError: When file exceeds max_size_bytes.
            EncryptedPDFError: When password-encrypted.
            EmptyPDFError: When text cannot be extracted (scanned or blank).
            PDFProcessingError: When the file is corrupt or malformed.
        """
        stream = None

        if isinstance(pdf_source, str):
            if not os.path.exists(pdf_source):
                raise PDFProcessingError(f"File not found: {pdf_source}")
            file_size = os.path.getsize(pdf_source)
            if file_size > max_size_bytes:
                raise FileSizeExceededError(
                    f"File size ({file_size / (1024 * 1024):.2f} MB) exceeds maximum allowed limit of {max_size_bytes / (1024 * 1024):.0f} MB."
                )
            try:
                stream = open(pdf_source, "rb")
            except Exception as e:
                raise PDFProcessingError(f"Could not open file: {e}")
        elif isinstance(pdf_source, bytes):
            if len(pdf_source) > max_size_bytes:
                raise FileSizeExceededError(
                    f"File size ({len(pdf_source) / (1024 * 1024):.2f} MB) exceeds maximum allowed limit of {max_size_bytes / (1024 * 1024):.0f} MB."
                )
            stream = io.BytesIO(pdf_source)
        elif hasattr(pdf_source, "read"):
            # Ensure read pointer is at start for Streamlit UploadedFile
            if hasattr(pdf_source, "seek"):
                try:
                    pdf_source.seek(0)
                except Exception:
                    pass

            size = getattr(pdf_source, "size", None)
            if size is not None and size > max_size_bytes:
                raise FileSizeExceededError(
                    f"File size ({size / (1024 * 1024):.2f} MB) exceeds maximum allowed limit of {max_size_bytes / (1024 * 1024):.0f} MB."
                )
            data = pdf_source.read()

            if hasattr(pdf_source, "seek"):
                try:
                    pdf_source.seek(0)
                except Exception:
                    pass

            if len(data) > max_size_bytes:
                raise FileSizeExceededError(
                    f"File size ({len(data) / (1024 * 1024):.2f} MB) exceeds maximum allowed limit of {max_size_bytes / (1024 * 1024):.0f} MB."
                )
            stream = io.BytesIO(data)
        else:
            raise PDFProcessingError("Unsupported PDF source type.")

        try:
            reader = PdfReader(stream)
            if reader.is_encrypted:
                try:
                    decrypted = reader.decrypt("")
                    if not decrypted:
                        raise EncryptedPDFError("The PDF is encrypted with a password. Please provide an unencrypted PDF.")
                except Exception:
                    raise EncryptedPDFError("The PDF is encrypted with a password. Please provide an unencrypted PDF.")

            extracted_text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text_parts.append(page_text)

            full_text = "\n".join(extracted_text_parts).strip()

            if not full_text or len(full_text) < 20:
                raise EmptyPDFError(
                    "No readable text could be found in the uploaded PDF. "
                    "If this is a scanned document or image-only PDF, please use a PDF containing selectable text."
                )

            return full_text

        except (EncryptedPDFError, EmptyPDFError, FileSizeExceededError):
            raise
        except PdfReadError as e:
            raise PDFProcessingError(f"Corrupted or invalid PDF format: {e}")
        except Exception as e:
            raise PDFProcessingError(f"Failed to process PDF: {e}")
        finally:
            if isinstance(pdf_source, str) and stream:
                stream.close()
