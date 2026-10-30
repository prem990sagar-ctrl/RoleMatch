"""
Models Package: Houses domain entities, data loaders, and machine learning business logic.
"""
from models.entities import JobRole, RecommendationResult, ResumeProfile
from models.pdf_model import (
    PDFModel,
    PDFProcessingError,
    FileSizeExceededError,
    EncryptedPDFError,
    EmptyPDFError,
    MAX_FILE_SIZE_BYTES
)
from models.skill_model import SkillModel, COMMON_SKILL_ALIASES
from models.recommender_model import RecommenderModel, calculate_overall_score

__all__ = [
    "JobRole",
    "RecommendationResult",
    "ResumeProfile",
    "PDFModel",
    "PDFProcessingError",
    "FileSizeExceededError",
    "EncryptedPDFError",
    "EmptyPDFError",
    "MAX_FILE_SIZE_BYTES",
    "SkillModel",
    "COMMON_SKILL_ALIASES",
    "RecommenderModel",
    "calculate_overall_score",
]

