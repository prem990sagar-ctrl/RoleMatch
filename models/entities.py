"""
Module: models/entities.py
Purpose: Domain data structures (entities) representing core business models.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Set


@dataclass
class JobRole:
    """Represents a single job posting record from the genuine dataset."""
    job_id: int
    job_title: str
    company_name: Optional[str]
    category: str
    job_skill_set: List[str] = field(default_factory=list)
    job_description: str = ""


@dataclass
class ResumeProfile:
    """Represents candidate resume text and extracted skills."""
    raw_text: str
    detected_skills: Set[str] = field(default_factory=set)
    file_name: Optional[str] = None
    file_size_bytes: int = 0


@dataclass
class Course:
    """Represents an educational course recommendation."""
    id: str
    title: str
    provider: str
    instructor: str
    level: str
    duration: str
    url: str
    skills_covered: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class CareerPathStep:
    """Represents a sequential step in the greedy personalized career path."""
    step_number: int
    course: Course
    covered_gap_skills: List[str] = field(default_factory=list)


@dataclass
class RecommendationResult:
    """Represents an explainable role recommendation output."""
    rank: int
    job_id: int
    job_title: str
    company_name: Optional[str]
    category: str
    overall_score: float
    text_similarity_score: float
    skill_coverage_score: float
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    total_role_skills: int = 0
    description_snippet: str = ""
    company_location: str = "Remote"
    recommended_courses: List[dict] = field(default_factory=list)

