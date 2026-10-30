"""
Unit tests for skill_extractor module.
"""
import pytest
from utils.skill_extractor import (
    extract_skills,
    normalize_skill_string,
    build_skill_pattern,
    COMMON_SKILL_ALIASES,
)


def test_basic_skill_extraction():
    dataset_skills = {"Python", "SQL", "Machine Learning", "Docker", "Java"}
    resume_text = """
    Software Engineer with 3 years of experience.
    Proficient in Python, SQL, and Docker.
    Built automated data pipelines.
    """
    detected = extract_skills(resume_text, dataset_skills=dataset_skills)
    assert "Python" in detected
    assert "SQL" in detected
    assert "Docker" in detected
    assert "Java" not in detected


def test_alias_mapping():
    dataset_skills = {"Machine Learning", "JavaScript", "Natural Language Processing", "Kubernetes"}
    resume_text = "Experienced in ML, JS, NLP, and K8s container orchestration."
    detected = extract_skills(resume_text, dataset_skills=dataset_skills)
    
    # Should resolve aliases to canonical forms
    assert "Machine Learning" in detected
    assert "JavaScript" in detected
    assert "Natural Language Processing" in detected
    assert "Kubernetes" in detected


def test_word_boundaries_no_false_matches():
    dataset_skills = {"C", "Go", "Java", "Ruby"}
    # The words 'Good', 'JavaScript', 'Catch' should not trigger 'Go', 'Java', or 'C'
    resume_text = "I have Good communication skills and love JavaScript and Catch-up meetings."
    detected = extract_skills(resume_text, dataset_skills=dataset_skills)
    assert "Go" not in detected
    assert "Java" not in detected
    assert "C" not in detected


def test_symbols_cplusplus_and_csharp():
    dataset_skills = {"C++", "C#", ".NET", "Node.js"}
    resume_text = "Proficient in C++, C#, and .NET runtime environments. Built servers with Node.js."
    detected = extract_skills(resume_text, dataset_skills=dataset_skills)
    assert "C++" in detected
    assert "C#" in detected
    assert ".NET" in detected
    assert "Node.js" in detected


def test_empty_and_whitespace_text():
    assert extract_skills("") == set()
    assert extract_skills("   \n\t  ") == set()
    assert extract_skills(None) == set()


def test_normalize_skill_string():
    raw_bracketed = "['Python', 'Machine Learning', 'AWS']"
    normalized = normalize_skill_string(raw_bracketed)
    assert normalized == ["Python", "Machine Learning", "AWS"]

    raw_csv = "Python, SQL, Tableau"
    normalized_csv = normalize_skill_string(raw_csv)
    assert normalized_csv == ["Python", "SQL", "Tableau"]

    assert normalize_skill_string("") == []
    assert normalize_skill_string(None) == []

