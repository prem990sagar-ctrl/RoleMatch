"""
Unit tests for pdf_extractor module.
"""
import io
import pytest
from utils.pdf_extractor import (
    extract_text_from_pdf,
    PDFProcessingError,
    FileSizeExceededError,
    EmptyPDFError,
)

SAMPLE_VALID_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
    b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
    b"3 0 obj << /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> "
    b"/MediaBox [0 0 612 792] /Contents 5 0 R >> endobj\n"
    b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
    b"5 0 obj << /Length 55 >> stream\n"
    b"BT\n"
    b"/F1 12 Tf\n"
    b"100 700 Td\n"
    b"(Python Developer Resume Data Science and Machine Learning) Tj\n"
    b"ET\n"
    b"endstream\n"
    b"endobj\n"
    b"xref\n"
    b"0 6\n"
    b"0000000000 65535 f \n"
    b"0000000009 00000 n \n"
    b"0000000058 00000 n \n"
    b"0000000115 00000 n \n"
    b"0000000244 00000 n \n"
    b"0000000319 00000 n \n"
    b"trailer << /Size 6 /Root 1 0 R >>\n"
    b"startxref\n"
    b"425\n"
    b"%%EOF"
)

SAMPLE_EMPTY_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
    b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
    b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >> endobj\n"
    b"xref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n"
    b"trailer << /Size 4 /Root 1 0 R >>\nstartxref\n185\n%%EOF"
)


def test_extract_text_from_valid_pdf_bytes():
    text = extract_text_from_pdf(SAMPLE_VALID_PDF)
    assert "Python Developer Resume" in text
    assert "Data Science" in text


def test_extract_text_from_bytes_io():
    stream = io.BytesIO(SAMPLE_VALID_PDF)
    text = extract_text_from_pdf(stream)
    assert "Python Developer" in text


def test_empty_pdf_raises_empty_pdf_error():
    with pytest.raises(EmptyPDFError) as exc_info:
        extract_text_from_pdf(SAMPLE_EMPTY_PDF)
    assert "No readable text could be found" in str(exc_info.value)


def test_file_size_exceeded():
    large_bytes = b"0" * 1024
    with pytest.raises(FileSizeExceededError):
        extract_text_from_pdf(large_bytes, max_size_bytes=512)


def test_corrupted_pdf_raises_error():
    corrupted_data = b"NOT_A_REAL_PDF_HEADER_DATA"
    with pytest.raises(PDFProcessingError):
        extract_text_from_pdf(corrupted_data)


def test_nonexistent_file_path():
    with pytest.raises(PDFProcessingError):
        extract_text_from_pdf("non_existent_file_path.pdf")

