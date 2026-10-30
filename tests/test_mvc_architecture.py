"""
Unit tests specifically validating the Model-View-Controller (MVC) architecture.
"""
import io
import pytest
import pandas as pd
import streamlit as st
from models.entities import JobRole, RecommendationResult, ResumeProfile
from models.pdf_model import PDFModel, EmptyPDFError
from models.skill_model import SkillModel
from models.recommender_model import RecommenderModel, calculate_overall_score
from controllers.app_controller import AppController


def test_entities_instantiation():
    """Verify data models and entity structures."""
    role = JobRole(
        job_id=101,
        job_title="AI Engineer",
        company_name="DeepMind",
        category="INFORMATION-TECHNOLOGY",
        job_skill_set=["Python", "TensorFlow"],
        job_description="Research and develop cutting-edge models."
    )
    assert role.job_id == 101
    assert role.job_title == "AI Engineer"

    result = RecommendationResult(
        rank=1,
        job_id=101,
        job_title="AI Engineer",
        company_name="DeepMind",
        category="INFORMATION-TECHNOLOGY",
        overall_score=85.5,
        text_similarity_score=80.0,
        skill_coverage_score=91.0,
        matched_skills=["Python", "TensorFlow"],
        missing_skills=[],
        total_role_skills=2
    )
    assert result.rank == 1
    assert result.overall_score == 85.5


def test_skill_model_mvc():
    """Verify SkillModel logic in the Model layer."""
    vocab = {"Python", "SQL", "Docker", "Machine Learning"}
    model = SkillModel(vocabulary=vocab)
    detected = model.extract("Software developer with strong ML and Python background.")
    assert "Python" in detected
    assert "Machine Learning" in detected  # via alias resolution


def test_recommender_model_mvc():
    """Verify RecommenderModel in the Model layer."""
    df = pd.DataFrame([
        {
            "job_id": 1,
            "job_title": "Python Backend Engineer",
            "company_name": "",
            "category": "INFORMATION-TECHNOLOGY",
            "job_skill_set": "Python, SQL, Django",
            "job_description": "Develop backend web services using Python and SQL."
        }
    ])
    model = RecommenderModel(df)
    results = model.recommend(
        resume_text="Senior Python and SQL developer.",
        detected_resume_skills={"Python", "SQL"},
        top_k=1
    )
    assert len(results) == 1
    rec = results[0]
    assert isinstance(rec, RecommendationResult)
    assert rec.job_title == "Python Backend Engineer"
    assert rec.overall_score > 50.0


def test_controller_initialization():
    """Verify AppController initializes correctly with models."""
    controller = AppController()
    assert controller.df is not None
    assert len(controller.df) >= 1400  # Combined genuine base + Computer Science datasets
    assert controller.recommender is not None
    assert controller.skill_model is not None

    sample_titles = controller.get_sample_titles(count=5)
    assert len(sample_titles) == 5


def test_controller_toggle_theme():
    """Verify theme toggle changes session state correctly."""
    st.session_state["dark_mode"] = False
    controller = AppController()
    controller.toggle_theme()
    assert st.session_state["dark_mode"] is True
    controller.toggle_theme()
    assert st.session_state["dark_mode"] is False
