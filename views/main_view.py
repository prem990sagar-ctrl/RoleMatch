"""
Module: views/main_view.py
Purpose: Main View coordinator assembling pages, sidebars, and reactive components.
"""
from typing import List, Set, Optional, Callable
import streamlit as st
from views.theme import inject_custom_css
from views.components import UIComponents
from models.entities import RecommendationResult, CareerPathStep


class MainView:
    """View Coordinator for RoleMatch AI."""

    @staticmethod
    def render_base(dark_mode: bool, on_toggle_theme: Optional[Callable[[], None]] = None):
        """Render theme stylesheet, sidebar branding, and header with theme toggle."""
        # 1. Inject Theme Styles First
        inject_custom_css(dark_mode)

        # 2. Render Sidebar
        UIComponents.render_sidebar()

        # 3. Render Header with Theme Toggle Button
        UIComponents.render_header(dark_mode, on_toggle_clicked=on_toggle_theme)

    @staticmethod
    def render_resume_uploader():
        """Render the resume file uploader directly between header and content."""
        return UIComponents.render_main_resume_uploader()

    @staticmethod
    def render_sidebar_uploader():
        """Backward-compatible fallback for uploader."""
        return UIComponents.render_main_resume_uploader()

    @staticmethod
    def render_landing_page(sample_titles: List[str]):
        """Render the welcome landing page."""
        UIComponents.render_landing_page(sample_titles)

    @staticmethod
    def render_tabs_view(
        detected_skills: Set[str],
        recommendations: List[RecommendationResult],
        career_path: List[CareerPathStep],
        resume_snippet: str = ""
    ):
        """Render the 3 main tabs: Skill Profile, Job Matches, Career Path."""
        UIComponents.render_tabs_view(
            detected_skills=detected_skills,
            recommendations=recommendations,
            career_path=career_path,
            resume_snippet=resume_snippet
        )

    @staticmethod
    def render_error_state(error_message: str):
        """Render error message and info box."""
        st.error(error_message)
        UIComponents.render_info_box()

    # Backward compatibility aliases
    @staticmethod
    def render_empty_state(sample_titles: List[str]):
        UIComponents.render_landing_page(sample_titles)

    @staticmethod
    def render_results(detected_skills: Set[str], recommendations: List[RecommendationResult]):
        UIComponents.render_tabs_view(detected_skills, recommendations, [], "")
