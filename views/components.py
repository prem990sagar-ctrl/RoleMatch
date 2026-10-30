"""
Module: views/components.py
Purpose: Modular UI presentation components for Streamlit rendering.
         Implements exact layout for:
         - Header & Landing Page (AI Career Path & Skill-Gap Recommender)
         - Tab 1: Skill Profile
         - Tab 2: Job Matches (Fit %, Progress bar, Matched skills, Skill gap, Recommended courses)
         - Tab 3: Career Path (Greedy set-cover sequential learning path)
"""
from pathlib import Path
from typing import List, Set, Optional, Callable, Dict
import streamlit as st
from models.entities import RecommendationResult, CareerPathStep, Course


class UIComponents:
    """Encapsulates reusable Streamlit visual components."""

    @staticmethod
    def render_header(dark_mode: bool, on_toggle_clicked: Optional[Callable[[], None]] = None):
        """Render the page title and quick theme toggle button."""
        col1, col2 = st.columns([4, 1.2], vertical_alignment="center")
        with col1:
            st.markdown("<div class='app-title'>AI Career Path & Skill-Gap Recommender</div>", unsafe_allow_html=True)
        with col2:
            btn_label = "Light Mode" if dark_mode else "Dark Mode"
            st.button(
                btn_label,
                key="header_theme_toggle_btn",
                use_container_width=True,
                on_click=on_toggle_clicked
            )

    @staticmethod
    def render_sidebar():
        """Render the sidebar branding, dataset attribution, and formula explanation."""
        st.sidebar.markdown(
            "<div class='sidebar-brand'><span class='brand-text'>RoleMatch</span> <span class='brand-accent'>AI</span></div>",
            unsafe_allow_html=True
        )

        st.sidebar.subheader("Datasets Used")
        st.sidebar.markdown("""
        - **Computer Science & IT Roles**:
          - `DevilsLord/It_job_roles_skills_certifications` (Top IT/CS Roles & Skills)
          - `jacob-hugging-face/job-descriptions` (Tech & Software Postings)
        - **Cross-Domain Career Roles**:
          - `batuhanmtl/job-skill-set` (LinkedIn Postings)
        - **Total Records**: 1,431 Roles & Postings
        - **Categories**: Computer Science, IT, Finance, HR, Sales, Business Development
        """)

    @staticmethod
    def render_main_resume_uploader():
        """Render the resume file uploader directly between header and content."""
        st.subheader("Upload Resume")
        uploaded = st.file_uploader(
            "Select your resume in PDF format (Maximum size: 10 MB)",
            type=["pdf"],
            key="main_pdf_uploader",
            help="Select a standard selectable PDF resume document."
        )
        return uploaded

    @staticmethod
    def render_landing_page(sample_titles: List[str]):
        """Render the empty-state landing page matching the reference application."""
        st.markdown("""
        ### Welcome to RoleMatch AI

        **Upload your resume PDF above** to get:
        - **Your extracted skill profile**
        - **Top matched jobs ranked by semantic fit**
        - **The skill gap for each job**
        - **Courses and an ordered career path to close those gaps**
        """)

        st.markdown("<br>", unsafe_allow_html=True)
        UIComponents.render_sample_resumes_section()

        if sample_titles:
            UIComponents.render_sample_roles_expander(sample_titles)

        UIComponents.render_info_box()

    @staticmethod
    def render_sample_resumes_section():
        """Render a section offering 5 sample resumes for quick testing and download."""
        sample_files = [
            ("1_software_engineer_resume.pdf", "Software Engineer", "IT & Cloud"),
            ("2_data_scientist_resume.pdf", "Data Scientist", "AI & Analytics"),
            ("3_financial_analyst_resume.pdf", "Financial Analyst", "Finance"),
            ("4_human_resources_resume.pdf", "HR Specialist", "Human Resources"),
            ("5_business_development_sales_resume.pdf", "Sales Executive", "Sales & Strategy")
        ]
        with st.expander("Need a test resume? Download sample PDF resumes"):
            st.caption("Click any button below to download a realistic sample resume for testing:")
            cols = st.columns(len(sample_files))
            for i, (fname, label, domain) in enumerate(sample_files):
                fpath = Path(__file__).resolve().parent.parent / "sample_resumes" / fname
                if fpath.is_file():
                    with fpath.open("rb") as f:
                        file_data = f.read()
                    with cols[i]:
                        st.download_button(
                            label=label,
                            data=file_data,
                            file_name=fname,
                            mime="application/pdf",
                            key=f"sample_dl_btn_{i}",
                            use_container_width=True
                        )
                        st.caption(domain)

    @staticmethod
    def render_sample_roles_expander(sample_titles: List[str]):
        """Render an expander showing genuine job titles available in the dataset."""
        with st.expander("Browse sample job titles available in dataset"):
            cols = st.columns(3)
            for i, title in enumerate(sample_titles):
                cols[i % 3].markdown(f"• **{title}**")

    @staticmethod
    def render_tabs_view(
        detected_skills: Set[str],
        recommendations: List[RecommendationResult],
        career_path: List[CareerPathStep],
        resume_snippet: str = ""
    ):
        """
        Render the 3 main tabs:
        1. Skill Profile
        2. Job Matches
        3. Career Path
        """
        tab_profile, tab_matches, tab_path = st.tabs(["Skill Profile", "Job Matches", "Career Path"])

        # Tab 1: Skill Profile
        with tab_profile:
            st.subheader("Extracted Skill Profile")
            st.caption("Technical and domain skills identified directly from your parsed resume text.")

            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Identified Skills", len(detected_skills))
            col_m2.metric("Target Career Roles", len(recommendations))
            col_m3.metric("Vocabulary Match Rate", f"{min(100, round((len(detected_skills)/30)*100))}%")

            if detected_skills:
                st.markdown("**All Identified Skills:**")
                skills_html = "".join([f"<span class='skill-pill-detected'>{s}</span>" for s in sorted(detected_skills)])
                st.markdown(f"<div style='margin-bottom: 1.5rem;'>{skills_html}</div>", unsafe_allow_html=True)
            else:
                st.warning("No skills from the dataset vocabulary were detected. Matches rely on textual TF-IDF similarity.")

            if resume_snippet:
                with st.expander("View Resume Text Excerpt"):
                    st.text(resume_snippet[:1500] + ("..." if len(resume_snippet) > 1500 else ""))

        # Tab 2: Job Matches
        with tab_matches:
            st.subheader("Top Job Matches")
            st.caption("Ranked by semantic textual fit and required skill coverage.")

            if not recommendations:
                st.warning("No role recommendations could be generated.")
            else:
                for rec in recommendations:
                    UIComponents.render_job_match_card(rec)

        # Tab 3: Career Path
        with tab_path:
            st.subheader("Your personalized career path")
            st.markdown(
                "<div style='color: #64748B; font-size: 0.95rem; margin-bottom: 1.5rem;'>"
                "Courses are chosen greedily to cover the most gap skills across your top matched jobs, then ordered by difficulty."
                "</div>",
                unsafe_allow_html=True
            )

            if not career_path:
                st.info("No skill gaps detected across your top matched roles! Your resume already covers all required skills.")
            else:
                for step in career_path:
                    UIComponents.render_career_step_card(step)

        # Transparency info box
        UIComponents.render_info_box()

    @staticmethod
    def render_job_match_card(rec: RecommendationResult):
        """Render a single job match card."""
        company_loc = rec.company_name if rec.company_name else "Remote"
        fit_percent = int(round(rec.overall_score))

        matched_str = ", ".join(rec.matched_skills) if rec.matched_skills else "None detected"
        gap_str = ", ".join(rec.missing_skills) if rec.missing_skills else "None (Fully covered)"

        st.markdown(f"""
        <div class='job-match-card'>
            <div class='job-card-header'>
                <div>
                    <div class='job-title-text'>{rec.job_title}</div>
                    <div class='job-company-text'>{company_loc}</div>
                </div>
                <div class='fit-box'>
                    <div class='fit-label'>Fit</div>
                    <div class='fit-value'>{fit_percent}%</div>
                </div>
            </div>
            <div class='fit-progress-wrapper'>
                <div class='fit-progress-label'>overall fit: {fit_percent}%</div>
                <div class='fit-progress-track'>
                    <div class='fit-progress-fill' style='width: {fit_percent}%;'></div>
                </div>
            </div>
            <div class='skills-detail-row'>
                <strong>Matched skills:</strong> {matched_str} &nbsp;&nbsp;&nbsp;&nbsp; 
                <strong>Skill gap:</strong> {gap_str}
            </div>
        """, unsafe_allow_html=True)

        # Recommended courses section
        if rec.recommended_courses:
            st.markdown("<div class='courses-container'><div class='courses-header'>Recommended courses to close this gap:</div>", unsafe_allow_html=True)
            for item in rec.recommended_courses:
                course: Course = item["course"]
                skill = item["skill"]
                st.markdown(
                    f"<div class='course-item'>• <a href='{course.url}' target='_blank'>{course.title}</a> — "
                    f"{course.provider} ({course.instructor}) ({course.level}, {course.duration}) covers <em>{skill}</em></div>",
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        if rec.description_snippet:
            with st.expander(f"View Job Description for {rec.job_title}"):
                st.write(rec.description_snippet)

        st.markdown("</div>", unsafe_allow_html=True)

    @staticmethod
    def render_career_step_card(step: CareerPathStep):
        """Render a step in the personalized career path matching Image 2."""
        c = step.course
        pills_html = "".join([f"<span class='covers-pill'>covers {s}</span>" for s in step.covered_gap_skills])

        st.markdown(f"""
        <div class='career-step-card'>
            <div class='career-step-title'>
                Step {step.step_number}: <a href='{c.url}' target='_blank'>{c.title}</a>
            </div>
            <div class='career-step-meta'>
                {c.provider} ({c.instructor}) - {c.level} - {c.duration}
            </div>
            <div>
                {pills_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_info_box():
        """Render educational transparency notice and methodology explanation."""
        st.markdown("""
        <div class='info-box'>
            <b>How Recommendations Are Calculated (MVC Model Layer):</b><br>
            1. <b>TF-IDF Vectorization & Cosine Similarity (50%)</b>: 
               Converts resume text and job descriptions into numerical term-frequency vectors and calculates cosine similarity (0–100%).
            <br>
            2. <b>Skill Coverage (50%)</b>:
               Measures the percentage of required role skills found in the candidate's resume: 
               <code>(Matched Skills / Total Listed Role Skills) × 100</code>.
            <br>
            3. <b>Greedy Career Path Optimization</b>:
               Courses are chosen greedily using the classic set-cover algorithm to maximize gap skills covered per course,
               then ordered sequentially by prerequisite difficulty (Beginner → Intermediate → Advanced).
        </div>
        """, unsafe_allow_html=True)
