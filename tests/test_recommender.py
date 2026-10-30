"""
Unit tests for recommender module and dataset integration.
"""
import os
import pytest
import pandas as pd
from utils.recommender import (
    JobRoleRecommender,
    calculate_overall_score,
    prepare_job_text_corpus
)
from utils.skill_extractor import extract_skills


@pytest.fixture
def sample_jobs_df():
    """Create a sample mini job DataFrame for fast deterministic unit tests."""
    data = [
        {
            "job_id": 101,
            "job_title": "Python Developer",
            "company_name": "Tech Corp",
            "category": "INFORMATION-TECHNOLOGY",
            "job_skill_set": "Python, SQL, Django, Docker, Git",
            "job_description": "We are looking for a Python Developer to build REST APIs and scalable backend services with Django and PostgreSQL."
        },
        {
            "job_id": 102,
            "job_title": "Machine Learning Engineer",
            "company_name": "AI Labs",
            "category": "INFORMATION-TECHNOLOGY",
            "job_skill_set": "Python, Machine Learning, TensorFlow, PyTorch, Scikit-Learn, SQL",
            "job_description": "Join our AI research team as a Machine Learning Engineer developing deep learning neural networks and predictive analytics models."
        },
        {
            "job_id": 103,
            "job_title": "Financial Accountant",
            "company_name": "Finance Hub",
            "category": "FINANCE",
            "job_skill_set": "Financial Accounting, Tax Preparation, GAAP, Excel, Auditing",
            "job_description": "Responsible for managing quarterly financial statements, budget balancing, tax compliance, and auditing."
        },
        {
            "job_id": 104,
            "job_title": "Human Resources Specialist",
            "company_name": "",
            "category": "HR",
            "job_skill_set": "Recruitment, Employee Relations, Onboarding, Talent Acquisition",
            "job_description": "Manage recruitment pipeline, candidate screening, employee onboarding, and talent acquisition operations."
        },
        {
            "job_id": 105,
            "job_title": "Frontend React Developer",
            "company_name": "Web Solutions",
            "category": "INFORMATION-TECHNOLOGY",
            "job_skill_set": "JavaScript, TypeScript, React, HTML, CSS, Redux",
            "job_description": "Design and build interactive responsive web frontend interfaces using React, TypeScript, and modern CSS frameworks."
        },
        {
            "job_id": 106,
            "job_title": "Role Without Skills Listed",
            "company_name": "Generic Co",
            "category": "BUSINESS-DEVELOPMENT",
            "job_skill_set": "",
            "job_description": "General business operations position."
        }
    ]
    return pd.DataFrame(data)


def test_calculate_overall_score():
    # 50% text (80.0) + 50% skills (60.0) = 70.0
    score = calculate_overall_score(80.0, 60.0)
    assert score == 70.0

    # 100% and 0%
    assert calculate_overall_score(100.0, 0.0) == 50.0

    # Clamping out-of-range inputs
    assert calculate_overall_score(150.0, -20.0) == 50.0


def test_zero_skills_avoids_division_by_zero(sample_jobs_df):
    """Verify that jobs with empty skill lists do not crash and produce 0.0 coverage."""
    recommender = JobRoleRecommender(sample_jobs_df)
    results = recommender.recommend(
        resume_text="General business operations manager.",
        detected_resume_skills={"management"},
        top_k=6
    )
    assert len(results) > 0
    # Find role without skills
    no_skills_role = next((r for r in results if r["job_id"] == 106), None)
    assert no_skills_role is not None
    assert no_skills_role["skill_coverage_score"] == 0.0
    assert no_skills_role["total_role_skills"] == 0


def test_python_ml_resume_recommendations(sample_jobs_df):
    """Test candidate with Python, SQL, and Machine Learning skills."""
    resume_text = """
    Experienced Software Engineer with strong background in Python, SQL, and Machine Learning.
    Built predictive models using TensorFlow and Scikit-Learn.
    Developed scalable database schemas and API integrations.
    """
    detected_skills = {"Python", "SQL", "Machine Learning", "TensorFlow", "Scikit-Learn"}
    recommender = JobRoleRecommender(sample_jobs_df)
    recommendations = recommender.recommend(resume_text, detected_skills, top_k=5)

    assert len(recommendations) <= 5
    top_role = recommendations[0]

    # Top role should be ML Engineer or Python Developer
    assert top_role["job_title"] in ["Machine Learning Engineer", "Python Developer"]
    assert top_role["overall_score"] > 30.0
    assert len(top_role["matched_skills"]) > 0
    assert "Python" in top_role["matched_skills"]


def test_unrelated_resume_recommendations(sample_jobs_df):
    """Test candidate with completely unrelated background (culinary/pastry)."""
    resume_text = """
    Head Pastry Chef with 10 years of experience in French baking, sourdough fermentation,
    cake decorating, oven temperature calibration, and kitchen inventory management.
    """
    detected_skills = set()
    recommender = JobRoleRecommender(sample_jobs_df)
    recommendations = recommender.recommend(resume_text, detected_skills, top_k=5)

    assert len(recommendations) <= 5
    for rec in recommendations:
        # All matched skills should be empty and skill coverage should be 0
        assert rec["matched_skills"] == []
        assert rec["skill_coverage_score"] == 0.0


def test_empty_dataset_handling():
    """Verify graceful handling when dataset is empty."""
    empty_df = pd.DataFrame(columns=["job_id", "job_title", "company_name", "category", "job_skill_set", "job_description"])
    recommender = JobRoleRecommender(empty_df)
    results = recommender.recommend("Python developer resume", {"Python"}, top_k=5)
    assert results == []


def test_real_dataset_integrity():
    """Verify the real downloaded dataset in data/job_skill_set.csv."""
    dataset_path = os.path.join("data", "job_skill_set.csv")
    assert os.path.exists(dataset_path), f"Dataset file missing at {dataset_path}"

    df = pd.read_csv(dataset_path)
    assert len(df) == 1431, f"Expected 1431 records, got {len(df)}"

    expected_cols = ["job_id", "job_title", "company_name", "category", "job_skill_set", "job_description"]
    for col in expected_cols:
        assert col in df.columns, f"Missing column {col} in dataset"

    # Verify no empty job titles
    assert df["job_title"].isna().sum() == 0
    assert (df["job_title"].str.strip() == "").sum() == 0

    # Verify categories match expected genuine categories
    unique_cats = set(df["category"].dropna().unique())
    assert "COMPUTER-SCIENCE" in unique_cats
    assert "INFORMATION-TECHNOLOGY" in unique_cats
    assert "BUSINESS-DEVELOPMENT" in unique_cats
    assert "FINANCE" in unique_cats
    assert "HR" in unique_cats
    assert "SALES" in unique_cats

