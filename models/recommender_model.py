"""
Module: models/recommender_model.py
Purpose: Recommendation model utilizing TF-IDF, Cosine Similarity, and Skill Coverage heuristics.
"""
from typing import List, Dict, Any, Set, Optional
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.entities import RecommendationResult


def calculate_overall_score(
    text_similarity_score: float,
    skill_coverage_score: float,
    weight_text: float = 0.5,
    weight_skills: float = 0.5
) -> float:
    """
    Calculate explainable overall match score (0 - 100 scale).

    Formula:
        Overall Match Score = (weight_text * Text Similarity) + (weight_skills * Skill Coverage)
    """
    clamped_text = max(0.0, min(100.0, float(text_similarity_score)))
    clamped_skills = max(0.0, min(100.0, float(skill_coverage_score)))
    overall = (weight_text * clamped_text) + (weight_skills * clamped_skills)
    return round(float(overall), 2)


def prepare_job_text_corpus(df: pd.DataFrame) -> List[str]:
    """Combine job title, category, skills, and description into a unified text corpus."""
    corpus = []
    for _, row in df.iterrows():
        title = str(row.get("job_title", "") or "")
        category = str(row.get("category", "") or "")
        desc = str(row.get("job_description", "") or "")
        skills = str(row.get("job_skill_set", "") or "")
        corpus.append(f"{title} {category} {skills} {desc}".strip())
    return corpus


class RecommenderModel:
    """Core Machine Learning Model for role recommendations."""

    def __init__(self, df: pd.DataFrame, weight_text: float = 0.5, weight_skills: float = 0.5):
        self.df = df.copy().reset_index(drop=True)
        self.weight_text = weight_text
        self.weight_skills = weight_skills

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2)
        )

        if not self.df.empty:
            corpus = prepare_job_text_corpus(self.df)
            self.job_tfidf_matrix = self.vectorizer.fit_transform(corpus)
        else:
            self.job_tfidf_matrix = None

    def recommend(
        self,
        resume_text: str,
        detected_resume_skills: Set[str],
        top_k: int = 5
    ) -> List[RecommendationResult]:
        """
        Rank top matching job roles for a resume.

        Args:
            resume_text: Raw resume plain text.
            detected_resume_skills: Set of skills detected in resume.
            top_k: Number of recommendations to return (default 5).

        Returns:
            List of RecommendationResult entities.
        """
        if self.df.empty or self.job_tfidf_matrix is None or not resume_text.strip():
            return []

        # 1. TF-IDF Text Similarity
        resume_vec = self.vectorizer.transform([resume_text])
        cos_similarities = cosine_similarity(resume_vec, self.job_tfidf_matrix)[0]

        resume_skills_lower = {s.lower() for s in detected_resume_skills}
        candidates: List[RecommendationResult] = []

        for idx, row in self.df.iterrows():
            text_sim_0_1 = float(cos_similarities[idx])
            text_sim_score = round(max(0.0, min(100.0, text_sim_0_1 * 100.0)), 2)

            # 2. Skill Coverage Calculation
            raw_skills = row.get("job_skill_set", "")
            if isinstance(raw_skills, list):
                role_skills = [str(s).strip() for s in raw_skills if str(s).strip()]
            elif isinstance(raw_skills, str) and raw_skills.strip():
                parts = [p.strip().strip("'\"[]") for p in raw_skills.split(",")]
                role_skills = [p for p in parts if p]
            else:
                role_skills = []

            matched_skills = []
            missing_skills = []
            for rs in role_skills:
                if rs.lower() in resume_skills_lower:
                    matched_skills.append(rs)
                else:
                    missing_skills.append(rs)

            total_role_skills = len(role_skills)
            if total_role_skills > 0:
                skill_coverage_score = round((len(matched_skills) / total_role_skills) * 100.0, 2)
            else:
                skill_coverage_score = 0.0

            # 3. Overall Match Score
            overall_score = calculate_overall_score(
                text_similarity_score=text_sim_score,
                skill_coverage_score=skill_coverage_score,
                weight_text=self.weight_text,
                weight_skills=self.weight_skills
            )

            # Company name handling
            company_raw = row.get("company_name", None)
            if pd.isna(company_raw) or not str(company_raw).strip() or str(company_raw).lower() == "nan":
                company_name = None
            else:
                company_name = str(company_raw).strip()

            desc_raw = str(row.get("job_description", "") or "").strip()
            desc_snippet = (desc_raw[:220] + "...") if len(desc_raw) > 220 else desc_raw

            candidates.append(
                RecommendationResult(
                    rank=0,
                    job_id=int(row.get("job_id", idx)),
                    job_title=str(row.get("job_title", "Untitled Role")).strip(),
                    company_name=company_name,
                    category=str(row.get("category", "General")).strip(),
                    overall_score=overall_score,
                    text_similarity_score=text_sim_score,
                    skill_coverage_score=skill_coverage_score,
                    matched_skills=matched_skills,
                    missing_skills=missing_skills,
                    total_role_skills=total_role_skills,
                    description_snippet=desc_snippet
                )
            )

        # 4. Sort and assign ranks
        candidates.sort(key=lambda r: (r.overall_score, r.text_similarity_score), reverse=True)
        top_results = candidates[:top_k]
        for rank_idx, item in enumerate(top_results, start=1):
            item.rank = rank_idx

        return top_results

