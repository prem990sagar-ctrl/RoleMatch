"""
Module: utils/recommender.py
Purpose: Backward-compatible adapter delegating to models.recommender_model.RecommenderModel.
"""
from typing import List, Dict, Any, Set
import pandas as pd
from models.recommender_model import (
    RecommenderModel,
    calculate_overall_score,
    prepare_job_text_corpus
)
from models.entities import RecommendationResult


class JobRoleRecommender:
    """Adapter wrapping RecommenderModel to preserve legacy dictionary interface."""

    def __init__(self, df: pd.DataFrame, weight_text: float = 0.5, weight_skills: float = 0.5):
        self._model = RecommenderModel(df, weight_text=weight_text, weight_skills=weight_skills)
        self.df = self._model.df
        self.vectorizer = self._model.vectorizer
        self.job_tfidf_matrix = self._model.job_tfidf_matrix

    def recommend(
        self,
        resume_text: str,
        detected_resume_skills: Set[str],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        results = self._model.recommend(resume_text, detected_resume_skills, top_k=top_k)
        # Convert RecommendationResult dataclasses to dicts for backward compatibility
        return [
            {
                "rank": r.rank,
                "job_id": r.job_id,
                "job_title": r.job_title,
                "company_name": r.company_name,
                "category": r.category,
                "overall_score": r.overall_score,
                "text_similarity_score": r.text_similarity_score,
                "skill_coverage_score": r.skill_coverage_score,
                "matched_skills": r.matched_skills,
                "missing_skills": r.missing_skills,
                "total_role_skills": r.total_role_skills,
                "description_snippet": r.description_snippet
            }
            for r in results
        ]
