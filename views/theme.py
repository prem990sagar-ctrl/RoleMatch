"""
Module: views/theme.py
Purpose: Dynamic UI theming engine for Light and Dark modes.
         Ensures crisp, high-contrast, fully adaptive font colors across all Streamlit components.
"""
import streamlit as st


def inject_custom_css(dark_mode: bool):
    """
    Inject theme-specific CSS into the Streamlit web document.
    Ensures all headings, paragraphs, labels, expanders, file uploaders,
    math formulas, markdown containers, badges, and skill pills match the active theme.
    """
    if dark_mode:
        css = """
        <style>
            /* =========================================================
               DARK THEME: FONT COLORS & BACKGROUNDS
               ========================================================= */

            /* Root App & Main Canvas */
            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stHeader"] {
                background-color: #0B0F19 !important;
                color: #E2E8F0 !important;
            }
            .main .block-container {
                padding-top: 1.8rem;
                padding-bottom: 3rem;
                max-width: 1100px;
            }

            /* Global Headings */
            h1, h2, h3, h4, h5, h6,
            [data-testid="stHeader"] *,
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3,
            [data-testid="stMarkdownContainer"] h4 {
                color: #F8FAFC !important;
            }

            /* Body Text, Paragraphs, Lists & Labels */
            p, label, li,
            [data-testid="stMarkdownContainer"] p,
            [data-testid="stMarkdownContainer"] li {
                color: #E2E8F0 !important;
            }

            /* Bold text across all markdown */
            strong, b,
            [data-testid="stMarkdownContainer"] strong,
            [data-testid="stMarkdownContainer"] b {
                color: #FFFFFF !important;
            }

            /* Captions & Subtitles */
            .stCaption,
            [data-testid="stCaptionContainer"],
            [data-testid="stCaptionContainer"] * {
                color: #94A3B8 !important;
            }

            /* KaTeX Math Formulas */
            .katex,
            .katex *,
            .katex-display * {
                color: #F8FAFC !important;
            }

            /* Main Header Title */
            .app-title {
                font-size: 2.2rem;
                font-weight: 700;
                color: #F8FAFC !important;
                margin-bottom: 1rem;
            }

            /* Sidebar Colors & Typography */
            [data-testid="stSidebar"] {
                background-color: #111827 !important;
                border-right: 1px solid #1F2937 !important;
            }
            .sidebar-brand {
                font-size: 2.15rem !important;
                font-weight: 800 !important;
                letter-spacing: -0.5px !important;
                line-height: 1.15 !important;
                padding-top: 0.2rem !important;
                padding-bottom: 0.9rem !important;
                margin-bottom: 0.9rem !important;
                border-bottom: 1px solid #1F2937 !important;
                display: flex !important;
                align-items: center !important;
                gap: 0.35rem !important;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            }
            .sidebar-brand .brand-text {
                color: #F8FAFC !important;
                font-weight: 800 !important;
            }
            .sidebar-brand .brand-accent {
                background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                font-weight: 900 !important;
                letter-spacing: 0.5px !important;
            }
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] h4 {
                color: #F8FAFC !important;
            }
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] li,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] span {
                color: #CBD5E1 !important;
            }
            [data-testid="stSidebar"] strong,
            [data-testid="stSidebar"] b {
                color: #FFFFFF !important;
            }
            [data-testid="stSidebar"] .stCaption,
            [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
                color: #94A3B8 !important;
            }
            [data-testid="stSidebar"] hr {
                border-color: #334155 !important;
            }

            /* Buttons */
            button,
            [data-testid="baseButton-secondary"],
            [data-testid="baseButton-primary"] {
                background-color: #1E293B !important;
                color: #F8FAFC !important;
                border: 1px solid #475569 !important;
                border-radius: 8px !important;
            }
            button:hover {
                background-color: #334155 !important;
                border-color: #64748B !important;
                color: #FFFFFF !important;
            }
            button p, button span, button div {
                color: #F8FAFC !important;
                font-weight: 600 !important;
            }

            /* Role Recommendation Card */
            .role-card {
                background-color: #1E293B !important;
                border: 1px solid #334155 !important;
                border-radius: 12px;
                padding: 1.4rem;
                margin-bottom: 1.2rem;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.4);
                transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
            }
            .role-card:hover {
                border-color: #475569 !important;
                box-shadow: 0 6px 12px -2px rgba(0,0,0,0.6);
            }
            .role-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: #F8FAFC !important;
            }
            .role-meta {
                font-size: 0.88rem;
                color: #94A3B8 !important;
                margin-top: 0.25rem;
            }
            .role-meta b {
                color: #F8FAFC !important;
            }
            .score-breakdown {
                margin-top: 0.85rem;
                font-size: 0.88rem;
                color: #CBD5E1 !important;
            }
            .score-breakdown b {
                color: #F8FAFC !important;
            }
            .score-breakdown code {
                background-color: #0F172A !important;
                color: #93C5FD !important;
                border: 1px solid #334155 !important;
                padding: 0.15rem 0.35rem;
                border-radius: 4px;
            }

            /* Badges & Metrics */
            .rank-badge {
                display: inline-block;
                background-color: #2563EB !important;
                color: #FFFFFF !important;
                font-size: 0.85rem;
                font-weight: 700;
                padding: 0.25rem 0.65rem;
                border-radius: 9999px;
                margin-right: 0.6rem;
            }
            .score-badge {
                display: inline-block;
                background-color: #1E1B4B !important;
                color: #C7D2FE !important;
                font-size: 0.95rem;
                font-weight: 700;
                padding: 0.35rem 0.85rem;
                border-radius: 8px;
                border: 1px solid #3730A3 !important;
            }

            /* Skill Pills (High-Contrast for Dark Background) */
            .skill-pill-matched {
                display: inline-block;
                background-color: #064E3B !important;
                color: #6EE7B7 !important;
                border: 1px solid #059669 !important;
                font-size: 0.82rem;
                font-weight: 600;
                padding: 0.2rem 0.55rem;
                border-radius: 6px;
                margin: 0.2rem;
            }
            .skill-pill-missing {
                display: inline-block;
                background-color: #1E293B !important;
                color: #CBD5E1 !important;
                border: 1px solid #334155 !important;
                font-size: 0.82rem;
                font-weight: 400;
                padding: 0.2rem 0.55rem;
                border-radius: 6px;
                margin: 0.2rem;
            }
            .skill-pill-detected {
                display: inline-block;
                background-color: #1E3A8A !important;
                color: #93C5FD !important;
                border: 1px solid #3B82F6 !important;
                font-size: 0.85rem;
                font-weight: 600;
                padding: 0.25rem 0.65rem;
                border-radius: 6px;
                margin: 0.2rem;
            }
            .empty-text {
                color: #94A3B8 !important;
                font-size: 0.85rem;
            }
            .more-count-badge {
                color: #94A3B8 !important;
                font-size: 0.8rem;
            }
            .all-covered-text {
                color: #34D399 !important;
                font-size: 0.85rem;
                font-weight: 600;
            }

            /* Info Box */
            .info-box {
                background-color: #1E293B !important;
                border: 1px solid #334155 !important;
                border-radius: 10px;
                padding: 1.1rem;
                font-size: 0.9rem;
                color: #CBD5E1 !important;
                margin-top: 1.5rem;
            }
            .info-box b, .info-box strong {
                color: #F8FAFC !important;
            }
            .info-box code {
                background-color: #0F172A !important;
                color: #93C5FD !important;
                padding: 0.15rem 0.35rem;
                border-radius: 4px;
                border: 1px solid #334155 !important;
            }

            /* File Uploader Widget */
            [data-testid="stFileUploader"] {
                background-color: #1E293B !important;
                border: 1px dashed #475569 !important;
                border-radius: 10px;
                padding: 0.6rem;
            }
            [data-testid="stFileUploader"] section {
                background-color: transparent !important;
            }
            [data-testid="stFileUploader"] p,
            [data-testid="stFileUploader"] span,
            [data-testid="stFileUploader"] div,
            [data-testid="stFileUploader"] small {
                color: #CBD5E1 !important;
            }
            [data-testid="stFileUploader"] button {
                background-color: #334155 !important;
                color: #F8FAFC !important;
                border: 1px solid #475569 !important;
            }

            /* Expanders */
            [data-testid="stExpander"] {
                background-color: #1E293B !important;
                border: 1px solid #334155 !important;
                border-radius: 8px !important;
            }
            [data-testid="stExpander"] summary {
                background-color: #1E293B !important;
                color: #F8FAFC !important;
            }
            [data-testid="stExpander"] summary span,
            [data-testid="stExpander"] summary p,
            [data-testid="stExpander"] summary svg {
                color: #F8FAFC !important;
                fill: #F8FAFC !important;
                font-weight: 600 !important;
            }
            [data-testid="stExpander"] [data-testid="stExpanderDetails"],
            [data-testid="stExpander"] details > div {
                background-color: #1E293B !important;
                color: #E2E8F0 !important;
            }
            [data-testid="stExpander"] [data-testid="stExpanderDetails"] *,
            [data-testid="stExpander"] details > div * {
                color: #E2E8F0 !important;
            }
            [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
            [data-testid="stExpander"] [data-testid="stMarkdownContainer"] li {
                color: #CBD5E1 !important;
            }
            /* Excerpt Preformatted & Monospace Text inside Expanders (Dark Mode) */
            div[data-testid="stText"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
                margin: 0 !important;
            }
            [data-testid="stExpander"] div[data-testid="stText"] pre,
            [data-testid="stExpander"] pre,
            div[data-testid="stText"] pre {
                background-color: #0F172A !important;
                color: #F1F5F9 !important;
                border: 1px solid #334155 !important;
                border-radius: 8px !important;
                padding: 0.75rem 1rem !important;
                margin: 0.25rem 0 !important;
                max-height: 250px !important;
                overflow-y: auto !important;
                white-space: pre-wrap !important;
                word-break: break-word !important;
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace !important;
                font-size: 0.84rem !important;
                line-height: 1.48 !important;
            }
            [data-testid="stExpander"] pre::-webkit-scrollbar,
            div[data-testid="stText"] pre::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            [data-testid="stExpander"] pre::-webkit-scrollbar-thumb,
            div[data-testid="stText"] pre::-webkit-scrollbar-thumb {
                background: #475569;
                border-radius: 3px;
            }
            [data-testid="stExpander"] div[data-testid="stText"] *,
            [data-testid="stExpander"] pre * {
                color: #F1F5F9 !important;
            }
            code {
                background-color: #0F172A !important;
                color: #38BDF8 !important;
                padding: 0.15rem 0.35rem !important;
                border-radius: 4px !important;
                font-size: 0.88rem !important;
            }

            /* System Alerts (info, warning, error) */
            div[data-testid="stAlert"] {
                background-color: #1E293B !important;
                border: 1px solid #334155 !important;
            }
            div[data-testid="stAlert"] p,
            div[data-testid="stAlert"] span {
                color: #E2E8F0 !important;
            }

            /* =========================================================
               JOB MATCHES CARD & CAREER PATH STYLES (DARK)
               ========================================================= */
            .job-match-card {
                background-color: #111827 !important;
                border: 1px solid #1F2937 !important;
                border-radius: 12px !important;
                padding: 1.5rem !important;
                margin-bottom: 1.5rem !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2) !important;
            }
            .job-card-header {
                display: flex !important;
                justify-content: space-between !important;
                align-items: flex-start !important;
                gap: 1rem !important;
            }
            .job-title-text {
                font-size: 1.45rem !important;
                font-weight: 700 !important;
                color: #F8FAFC !important;
                margin-bottom: 0.25rem !important;
            }
            .job-company-text {
                font-size: 0.95rem !important;
                color: #94A3B8 !important;
                margin-bottom: 0.8rem !important;
            }
            .fit-box {
                text-align: right !important;
                min-width: 80px !important;
            }
            .fit-label {
                font-size: 0.82rem !important;
                color: #94A3B8 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
            }
            .fit-value {
                font-size: 2.2rem !important;
                font-weight: 800 !important;
                color: #38BDF8 !important;
                line-height: 1 !important;
            }
            .fit-progress-wrapper {
                margin: 0.75rem 0 1.1rem 0 !important;
            }
            .fit-progress-label {
                font-size: 0.88rem !important;
                color: #94A3B8 !important;
                margin-bottom: 0.35rem !important;
            }
            .fit-progress-track {
                width: 100% !important;
                height: 7px !important;
                background-color: #1F2937 !important;
                border-radius: 9999px !important;
                overflow: hidden !important;
            }
            .fit-progress-fill {
                height: 100% !important;
                background: linear-gradient(90deg, #3B82F6, #60A5FA) !important;
                border-radius: 9999px !important;
            }
            .skills-detail-row {
                font-size: 0.95rem !important;
                line-height: 1.6 !important;
                margin-bottom: 0.75rem !important;
                color: #E2E8F0 !important;
            }
            .skills-detail-row strong {
                color: #FFFFFF !important;
            }
            .courses-container {
                margin-top: 1rem !important;
                padding-top: 0.9rem !important;
                border-top: 1px dashed #334155 !important;
            }
            .courses-header {
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                color: #F8FAFC !important;
                margin-bottom: 0.5rem !important;
            }
            .course-item {
                font-size: 0.92rem !important;
                line-height: 1.6 !important;
                margin-bottom: 0.35rem !important;
                color: #CBD5E1 !important;
            }
            .course-item a {
                color: #60A5FA !important;
                text-decoration: underline !important;
            }
            .course-item em {
                color: #93C5FD !important;
                font-style: normal !important;
                font-weight: 600 !important;
            }

            /* Career Path Step Cards (Dark) */
            .career-step-card {
                background-color: #111827 !important;
                border: 1px solid #1F2937 !important;
                border-radius: 12px !important;
                padding: 1.3rem !important;
                margin-bottom: 1.2rem !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2) !important;
            }
            .career-step-title {
                font-size: 1.2rem !important;
                font-weight: 700 !important;
                color: #F8FAFC !important;
                margin-bottom: 0.3rem !important;
            }
            .career-step-title a {
                color: #60A5FA !important;
                text-decoration: none !important;
            }
            .career-step-title a:hover {
                text-decoration: underline !important;
            }
            .career-step-meta {
                font-size: 0.92rem !important;
                color: #94A3B8 !important;
                margin-bottom: 0.75rem !important;
            }
            .covers-pill {
                display: inline-block !important;
                background-color: #064E3B !important;
                color: #6EE7B7 !important;
                border: 1px solid #059669 !important;
                font-size: 0.8rem !important;
                font-weight: 600 !important;
                padding: 0.2rem 0.65rem !important;
                border-radius: 6px !important;
                margin-right: 0.4rem !important;
            }

            /* Streamlit Tabs Styling */
            button[data-baseweb="tab"] {
                font-size: 1.05rem !important;
                font-weight: 600 !important;
                padding: 0.5rem 1rem !important;
                color: #94A3B8 !important;
            }
            button[data-baseweb="tab"][aria-selected="true"] {
                color: #38BDF8 !important;
                border-bottom: 2px solid #38BDF8 !important;
            }
        </style>
        """
    else:
        css = """
        <style>
            /* =========================================================
               LIGHT THEME: FONT COLORS & BACKGROUNDS
               ========================================================= */

            /* Root App & Main Canvas */
            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stHeader"] {
                background-color: #F8FAFC !important;
                color: #1E293B !important;
            }
            .main .block-container {
                padding-top: 1.8rem;
                padding-bottom: 3rem;
                max-width: 1100px;
            }

            /* Global Headings */
            h1, h2, h3, h4, h5, h6,
            [data-testid="stHeader"] *,
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3,
            [data-testid="stMarkdownContainer"] h4 {
                color: #0F172A !important;
            }

            /* Body Text, Paragraphs, Lists & Labels */
            p, label, li,
            [data-testid="stMarkdownContainer"] p,
            [data-testid="stMarkdownContainer"] li {
                color: #334155 !important;
            }

            /* Bold text across all markdown */
            strong, b,
            [data-testid="stMarkdownContainer"] strong,
            [data-testid="stMarkdownContainer"] b {
                color: #0F172A !important;
            }

            /* Captions & Subtitles */
            .stCaption,
            [data-testid="stCaptionContainer"],
            [data-testid="stCaptionContainer"] * {
                color: #64748B !important;
            }

            /* KaTeX Math Formulas */
            .katex,
            .katex *,
            .katex-display * {
                color: #0F172A !important;
            }

            /* Main Header Title */
            .app-title {
                font-size: 2.2rem;
                font-weight: 700;
                color: #0F172A !important;
                margin-bottom: 1rem;
            }

            /* Sidebar Colors & Typography */
            [data-testid="stSidebar"] {
                background-color: #FFFFFF !important;
                border-right: 1px solid #E2E8F0 !important;
            }
            .sidebar-brand {
                font-size: 2.15rem !important;
                font-weight: 800 !important;
                letter-spacing: -0.5px !important;
                line-height: 1.15 !important;
                padding-top: 0.2rem !important;
                padding-bottom: 0.9rem !important;
                margin-bottom: 0.9rem !important;
                border-bottom: 1px solid #E2E8F0 !important;
                display: flex !important;
                align-items: center !important;
                gap: 0.35rem !important;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            }
            .sidebar-brand .brand-text {
                color: #0F172A !important;
                font-weight: 800 !important;
            }
            .sidebar-brand .brand-accent {
                background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                font-weight: 900 !important;
                letter-spacing: 0.5px !important;
            }
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] h4 {
                color: #0F172A !important;
            }
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] li,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] span {
                color: #334155 !important;
            }
            [data-testid="stSidebar"] strong,
            [data-testid="stSidebar"] b {
                color: #0F172A !important;
            }
            [data-testid="stSidebar"] .stCaption,
            [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
                color: #64748B !important;
            }
            [data-testid="stSidebar"] hr {
                border-color: #E2E8F0 !important;
            }

            /* Buttons */
            button,
            [data-testid="baseButton-secondary"],
            [data-testid="baseButton-primary"] {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                border: 1px solid #CBD5E1 !important;
                border-radius: 8px !important;
            }
            button:hover {
                background-color: #F1F5F9 !important;
                border-color: #94A3B8 !important;
                color: #0F172A !important;
            }
            button p, button span, button div {
                color: #0F172A !important;
                font-weight: 600 !important;
            }

            /* Role Recommendation Card */
            .role-card {
                background-color: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 12px;
                padding: 1.4rem;
                margin-bottom: 1.2rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
            }
            .role-card:hover {
                border-color: #CBD5E1 !important;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08);
            }
            .role-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: #0F172A !important;
            }
            .role-meta {
                font-size: 0.88rem;
                color: #64748B !important;
                margin-top: 0.25rem;
            }
            .role-meta b {
                color: #0F172A !important;
            }
            .score-breakdown {
                margin-top: 0.85rem;
                font-size: 0.88rem;
                color: #475569 !important;
            }
            .score-breakdown b {
                color: #0F172A !important;
            }
            .score-breakdown code {
                background-color: #F1F5F9 !important;
                color: #1E293B !important;
                padding: 0.15rem 0.35rem;
                border-radius: 4px;
            }

            /* Badges & Metrics */
            .rank-badge {
                display: inline-block;
                background-color: #0F172A !important;
                color: #FFFFFF !important;
                font-size: 0.85rem;
                font-weight: 700;
                padding: 0.25rem 0.65rem;
                border-radius: 9999px;
                margin-right: 0.6rem;
            }
            .score-badge {
                display: inline-block;
                background-color: #EEF2FF !important;
                color: #3730A3 !important;
                font-size: 0.95rem;
                font-weight: 700;
                padding: 0.35rem 0.85rem;
                border-radius: 8px;
                border: 1px solid #C7D2FE !important;
            }

            /* Skill Pills (High-Contrast for Light Background) */
            .skill-pill-matched {
                display: inline-block;
                background-color: #ECFDF5 !important;
                color: #065F46 !important;
                border: 1px solid #A7F3D0 !important;
                font-size: 0.82rem;
                font-weight: 600;
                padding: 0.2rem 0.55rem;
                border-radius: 6px;
                margin: 0.2rem;
            }
            .skill-pill-missing {
                display: inline-block;
                background-color: #F8FAFC !important;
                color: #64748B !important;
                border: 1px solid #E2E8F0 !important;
                font-size: 0.82rem;
                font-weight: 400;
                padding: 0.2rem 0.55rem;
                border-radius: 6px;
                margin: 0.2rem;
            }
            .skill-pill-detected {
                display: inline-block;
                background-color: #EFF6FF !important;
                color: #1E40AF !important;
                border: 1px solid #BFDBFE !important;
                font-size: 0.85rem;
                font-weight: 600;
                padding: 0.25rem 0.65rem;
                border-radius: 6px;
                margin: 0.2rem;
            }
            .empty-text {
                color: #64748B !important;
                font-size: 0.85rem;
            }
            .more-count-badge {
                color: #64748B !important;
                font-size: 0.8rem;
            }
            .all-covered-text {
                color: #059669 !important;
                font-size: 0.85rem;
                font-weight: 600;
            }

            /* Info Box */
            .info-box {
                background-color: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 10px;
                padding: 1.1rem;
                font-size: 0.9rem;
                color: #334155 !important;
                margin-top: 1.5rem;
            }
            .info-box b, .info-box strong {
                color: #0F172A !important;
            }
            .info-box code {
                background-color: #F1F5F9 !important;
                color: #0F172A !important;
                padding: 0.15rem 0.35rem;
                border-radius: 4px;
            }

            /* File Uploader Widget */
            [data-testid="stFileUploader"] {
                background-color: #FFFFFF !important;
                border: 1px dashed #CBD5E1 !important;
                border-radius: 10px;
                padding: 0.6rem;
            }
            [data-testid="stFileUploader"] section {
                background-color: transparent !important;
            }
            [data-testid="stFileUploader"] p,
            [data-testid="stFileUploader"] span,
            [data-testid="stFileUploader"] div,
            [data-testid="stFileUploader"] small {
                color: #475569 !important;
            }
            [data-testid="stFileUploader"] button {
                background-color: #F8FAFC !important;
                color: #0F172A !important;
                border: 1px solid #CBD5E1 !important;
            }

            /* Expanders */
            [data-testid="stExpander"] {
                background-color: #FFFFFF !important;
                border: 1px solid #CBD5E1 !important;
                border-radius: 8px !important;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
            }
            [data-testid="stExpander"] summary {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
            }
            [data-testid="stExpander"] summary:hover {
                background-color: #F8FAFC !important;
            }
            [data-testid="stExpander"] summary span,
            [data-testid="stExpander"] summary p,
            [data-testid="stExpander"] summary svg {
                color: #0F172A !important;
                fill: #0F172A !important;
                font-weight: 600 !important;
            }
            [data-testid="stExpander"] [data-testid="stExpanderDetails"],
            [data-testid="stExpander"] details > div {
                background-color: #FFFFFF !important;
                color: #1E293B !important;
                padding-top: 0.5rem !important;
            }
            [data-testid="stExpander"] [data-testid="stExpanderDetails"] *,
            [data-testid="stExpander"] details > div * {
                color: #1E293B !important;
            }
            [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
            [data-testid="stExpander"] [data-testid="stMarkdownContainer"] li {
                color: #334155 !important;
            }
            /* Excerpt Preformatted & Monospace Text inside Expanders (Light Mode) */
            div[data-testid="stText"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
                margin: 0 !important;
            }
            [data-testid="stExpander"] div[data-testid="stText"] pre,
            [data-testid="stExpander"] pre,
            div[data-testid="stText"] pre {
                background-color: #F8FAFC !important;
                color: #0F172A !important;
                border: 1px solid #CBD5E1 !important;
                border-radius: 8px !important;
                padding: 0.75rem 1rem !important;
                margin: 0.25rem 0 !important;
                max-height: 250px !important;
                overflow-y: auto !important;
                white-space: pre-wrap !important;
                word-break: break-word !important;
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace !important;
                font-size: 0.84rem !important;
                line-height: 1.48 !important;
            }
            [data-testid="stExpander"] pre::-webkit-scrollbar,
            div[data-testid="stText"] pre::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            [data-testid="stExpander"] pre::-webkit-scrollbar-thumb,
            div[data-testid="stText"] pre::-webkit-scrollbar-thumb {
                background: #CBD5E1;
                border-radius: 3px;
            }
            [data-testid="stExpander"] div[data-testid="stText"] *,
            [data-testid="stExpander"] pre * {
                color: #0F172A !important;
            }
            code {
                background-color: #F1F5F9 !important;
                color: #0F172A !important;
                padding: 0.15rem 0.35rem !important;
                border-radius: 4px !important;
                font-size: 0.88rem !important;
            }

            /* System Alerts */
            div[data-testid="stAlert"] {
                background-color: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
            }
            div[data-testid="stAlert"] p,
            div[data-testid="stAlert"] span {
                color: #1E293B !important;
            }

            /* =========================================================
               JOB MATCHES CARD & CAREER PATH STYLES (LIGHT)
               ========================================================= */
            .job-match-card {
                background-color: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 12px !important;
                padding: 1.5rem !important;
                margin-bottom: 1.5rem !important;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
            }
            .job-card-header {
                display: flex !important;
                justify-content: space-between !important;
                align-items: flex-start !important;
                gap: 1rem !important;
            }
            .job-title-text {
                font-size: 1.45rem !important;
                font-weight: 700 !important;
                color: #0F172A !important;
                margin-bottom: 0.25rem !important;
            }
            .job-company-text {
                font-size: 0.95rem !important;
                color: #64748B !important;
                margin-bottom: 0.8rem !important;
            }
            .fit-box {
                text-align: right !important;
                min-width: 80px !important;
            }
            .fit-label {
                font-size: 0.82rem !important;
                color: #64748B !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
            }
            .fit-value {
                font-size: 2.2rem !important;
                font-weight: 800 !important;
                color: #2563EB !important;
                line-height: 1 !important;
            }
            .fit-progress-wrapper {
                margin: 0.75rem 0 1.1rem 0 !important;
            }
            .fit-progress-label {
                font-size: 0.88rem !important;
                color: #64748B !important;
                margin-bottom: 0.35rem !important;
            }
            .fit-progress-track {
                width: 100% !important;
                height: 7px !important;
                background-color: #E2E8F0 !important;
                border-radius: 9999px !important;
                overflow: hidden !important;
            }
            .fit-progress-fill {
                height: 100% !important;
                background: linear-gradient(90deg, #2563EB, #3B82F6) !important;
                border-radius: 9999px !important;
            }
            .skills-detail-row {
                font-size: 0.95rem !important;
                line-height: 1.6 !important;
                margin-bottom: 0.75rem !important;
                color: #334155 !important;
            }
            .skills-detail-row strong {
                color: #0F172A !important;
            }
            .courses-container {
                margin-top: 1rem !important;
                padding-top: 0.9rem !important;
                border-top: 1px dashed #E2E8F0 !important;
            }
            .courses-header {
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                color: #0F172A !important;
                margin-bottom: 0.5rem !important;
            }
            .course-item {
                font-size: 0.92rem !important;
                line-height: 1.6 !important;
                margin-bottom: 0.35rem !important;
                color: #334155 !important;
            }
            .course-item a {
                color: #2563EB !important;
                text-decoration: underline !important;
            }
            .course-item em {
                color: #1D4ED8 !important;
                font-style: normal !important;
                font-weight: 600 !important;
            }

            /* Career Path Step Cards (Light) */
            .career-step-card {
                background-color: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 12px !important;
                padding: 1.3rem !important;
                margin-bottom: 1.2rem !important;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
            }
            .career-step-title {
                font-size: 1.2rem !important;
                font-weight: 700 !important;
                color: #0F172A !important;
                margin-bottom: 0.3rem !important;
            }
            .career-step-title a {
                color: #2563EB !important;
                text-decoration: none !important;
            }
            .career-step-title a:hover {
                text-decoration: underline !important;
            }
            .career-step-meta {
                font-size: 0.92rem !important;
                color: #64748B !important;
                margin-bottom: 0.75rem !important;
            }
            .covers-pill {
                display: inline-block !important;
                background-color: #DCFCE7 !important;
                color: #15803D !important;
                border: 1px solid #86EFAC !important;
                font-size: 0.8rem !important;
                font-weight: 600 !important;
                padding: 0.2rem 0.65rem !important;
                border-radius: 6px !important;
                margin-right: 0.4rem !important;
            }

            /* Streamlit Tabs Styling */
            button[data-baseweb="tab"] {
                font-size: 1.05rem !important;
                font-weight: 600 !important;
                padding: 0.5rem 1rem !important;
                color: #64748B !important;
            }
            button[data-baseweb="tab"][aria-selected="true"] {
                color: #2563EB !important;
                border-bottom: 2px solid #2563EB !important;
            }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)
