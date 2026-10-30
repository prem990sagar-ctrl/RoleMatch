"""
Module: controllers/app_controller.py
Purpose: Application Controller coordinating workflow between Models and Views.
         Coordinates resume parsing, skill extraction, role matching,
         course gap recommendations, and greedy career path construction.
"""
import json
from pathlib import Path
from typing import Tuple, Set, Optional, List
import pandas as pd
import streamlit as st

from models.pdf_model import (
    PDFModel,
    PDFProcessingError,
    FileSizeExceededError,
    EncryptedPDFError,
    EmptyPDFError,
    MAX_FILE_SIZE_BYTES
)
from models.skill_model import SkillModel
from models.recommender_model import RecommenderModel
from models.course_model import CourseModel
from models.entities import RecommendationResult, CareerPathStep
from views.main_view import MainView

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "job_skill_set.csv"
VOCAB_PATH = PROJECT_ROOT / "data" / "skills_vocabulary.json"

SAMPLE_RESUMES_MAP = {
    "Alex Chen — Software Engineer": PROJECT_ROOT / "sample_resumes" / "1_software_engineer_resume.pdf",
    "Dr. Priya Sharma — Data Scientist / ML": PROJECT_ROOT / "sample_resumes" / "2_data_scientist_resume.pdf",
    "David Miller — Financial Analyst": PROJECT_ROOT / "sample_resumes" / "3_financial_analyst_resume.pdf",
    "Sarah Jenkins — HR Specialist": PROJECT_ROOT / "sample_resumes" / "4_human_resources_resume.pdf",
    "Michael Reynolds — Sales Executive": PROJECT_ROOT / "sample_resumes" / "5_business_development_sales_resume.pdf"
}


@st.cache_data
def _load_data_and_vocab() -> Tuple[Optional[pd.DataFrame], Set[str]]:
    """Cached loader for dataset DataFrame and skills vocabulary."""
    if not DATA_PATH.is_file():
        return None, set()

    df = pd.read_csv(DATA_PATH)
    vocab = set()
    if VOCAB_PATH.is_file():
        with VOCAB_PATH.open("r", encoding="utf-8") as f:
            vocab = set(json.load(f))
    else:
        for raw in df["job_skill_set"].dropna():
            for s in str(raw).split(","):
                item = s.strip()
                if item:
                    vocab.add(item)
    return df, vocab


@st.cache_resource
def _get_recommender_model(data_version: int) -> Optional[RecommenderModel]:
    """Cached factory for fitting and returning the RecommenderModel."""
    df, _ = _load_data_and_vocab()
    if df is None or df.empty:
        return None
    return RecommenderModel(df)


@st.cache_resource
def _get_course_model() -> CourseModel:
    """Cached factory for loading the course recommendation catalog."""
    return CourseModel()


class AppController:
    """Controller orchestrating interactions between Models and Views."""

    def __init__(self):
        # Initialize session state for theme
        if "dark_mode" not in st.session_state:
            st.session_state["dark_mode"] = False

        self.df, self.vocabulary = _load_data_and_vocab()
        if self.df is not None and not self.df.empty:
            self.recommender = _get_recommender_model(len(self.df))
            self.skill_model = SkillModel(vocabulary=self.vocabulary)
        else:
            self.recommender = None
            self.skill_model = None

        self.course_model = _get_course_model()

    def toggle_theme(self):
        """Callback to toggle theme state across the application."""
        st.session_state["dark_mode"] = not st.session_state.get("dark_mode", False)

    def get_sample_titles(self, count: int = 12) -> List[str]:
        """Fetch a sample of genuine job titles for preview."""
        if self.df is None or self.df.empty:
            return []
        return self.df["job_title"].dropna().sample(min(count, len(self.df)), random_state=42).tolist()

    def run(self):
        """Main execution loop of the controller."""
        dark_mode = st.session_state.get("dark_mode", False)

        # 1. Render Base Layout (CSS Theme, Sidebar branding, Header)
        MainView.render_base(dark_mode=dark_mode, on_toggle_theme=self.toggle_theme)

        # 2. Check Dataset Readiness
        if self.df is None or self.df.empty or self.recommender is None:
            MainView.render_error_state(
                "Job dataset not found! Please ensure data/job_skill_set.csv is present. "
                "You can generate it by running `python download_and_normalize_data.py`."
            )
            return

        # 3. Render Resume Input directly between Header and Content
        uploaded_file = MainView.render_resume_uploader()

        target_file_or_path = uploaded_file

        # If no resume provided, render welcome landing page
        if target_file_or_path is None:
            sample_titles = self.get_sample_titles()
            MainView.render_landing_page(sample_titles=sample_titles)
            return

        # 4. Extract Text from PDF (Model Layer)
        extracted_text = ""
        error_msg = None

        with st.spinner("Extracting text from resume PDF..."):
            try:
                extracted_text = PDFModel.extract_text(target_file_or_path, max_size_bytes=MAX_FILE_SIZE_BYTES)
            except FileSizeExceededError as e:
                error_msg = f"**File Size Limit Exceeded**: {e}"
            except EncryptedPDFError as e:
                error_msg = f"**Protected File**: {e}"
            except EmptyPDFError as e:
                error_msg = f"**Unreadable Content**: {e}"
            except PDFProcessingError as e:
                error_msg = f"**PDF Error**: {e}"
            except Exception as e:
                error_msg = f"An unexpected error occurred while reading the PDF: {e}"

        if error_msg:
            MainView.render_error_state(error_msg)
            return

        # 5. Extract Skills, Match Roles, and Recommend Courses (Model Layer)
        with st.spinner("Analyzing skill profile, matching jobs, and building career path..."):
            detected_skills = self.skill_model.extract(extracted_text)
            recommendations = self.recommender.recommend(
                resume_text=extracted_text,
                detected_resume_skills=detected_skills,
                top_k=5
            )

            # Attach recommended courses to each job match card
            all_gap_skills: List[str] = []
            for rec in recommendations:
                rec.recommended_courses = self.course_model.get_courses_for_skills(
                    missing_skills=rec.missing_skills,
                    max_courses=2
                )
                all_gap_skills.extend(rec.missing_skills)

            # Build greedy personalized career path
            career_path = self.course_model.build_greedy_career_path(
                all_gap_skills=all_gap_skills,
                max_steps=4
            )

        # 6. Render 3-Tab View: Skill Profile | Job Matches | Career Path
        MainView.render_tabs_view(
            detected_skills=detected_skills,
            recommendations=recommendations,
            career_path=career_path,
            resume_snippet=extracted_text
        )
