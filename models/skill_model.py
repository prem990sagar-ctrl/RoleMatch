"""
Module: models/skill_model.py
Purpose: Skill extraction model supporting boundary regex pattern matching,
         alias resolution, and dataset vocabulary normalization.
"""
import re
from typing import List, Set, Dict, Optional

# Alias dictionary for common technical skill abbreviations and variants
COMMON_SKILL_ALIASES: Dict[str, str] = {
    "js": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "ai": "Artificial Intelligence",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "k8s": "Kubernetes",
    "aws": "Amazon Web Services",
    "gcp": "Google Cloud Platform",
    "tf": "TensorFlow",
    "torch": "PyTorch",
    "postgres": "PostgreSQL",
    "mongo": "MongoDB",
    "sklearn": "Scikit-Learn",
    "bi": "Business Intelligence",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "reactjs": "React",
    "react.js": "React",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
    "angularjs": "Angular",
    "html5": "HTML",
    "css3": "CSS",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "rest": "REST API",
    "restful": "REST API",
    "rest api": "REST API",
    "restful api": "REST API",
    "nosql": "NoSQL",
}


class SkillModel:
    """Model responsible for extracting skills from text using vocabularies and aliases."""

    def __init__(self, vocabulary: Optional[Set[str]] = None, alias_dict: Optional[Dict[str, str]] = None):
        self.vocabulary = vocabulary if vocabulary is not None else set()
        self.alias_dict = alias_dict if alias_dict is not None else COMMON_SKILL_ALIASES
        self._compiled_patterns: Dict[str, re.Pattern] = {}

    @staticmethod
    def build_pattern(skill: str) -> re.Pattern:
        """
        Build regex pattern that respects boundaries, including symbols like C++, C#, .NET.
        """
        escaped = re.escape(skill)
        left_boundary = r"(?<![\w#+])" if skill and (skill[0].isalnum() or skill[0] == '.') else r""
        right_boundary = r"(?![\w#+])"
        return re.compile(f"{left_boundary}{escaped}{right_boundary}", re.IGNORECASE)

    def extract(self, text: str) -> Set[str]:
        """
        Extract technical and professional skills from text.

        Args:
            text: Raw plain text.

        Returns:
            Set of canonical/dataset skill names found in the text.
        """
        if not text or not text.strip():
            return set()

        text_clean = text.strip()
        detected: Set[str] = set()

        # 1. Match vocabulary skills
        for skill in self.vocabulary:
            if not skill or not skill.strip():
                continue
            skill_clean = skill.strip()
            if len(skill_clean) == 1 and skill_clean.upper() not in {"C", "R"}:
                continue

            if skill_clean not in self._compiled_patterns:
                self._compiled_patterns[skill_clean] = self.build_pattern(skill_clean)

            pattern = self._compiled_patterns[skill_clean]
            if pattern.search(text_clean):
                detected.add(skill_clean)

        # 2. Match alias triggers
        for alias, canonical in self.alias_dict.items():
            if alias not in self._compiled_patterns:
                self._compiled_patterns[alias] = self.build_pattern(alias)

            pattern = self._compiled_patterns[alias]
            if pattern.search(text_clean):
                # Map to dataset casing if present
                matched_in_vocab = False
                for v_skill in self.vocabulary:
                    if v_skill.lower() == canonical.lower():
                        detected.add(v_skill)
                        matched_in_vocab = True
                        break
                if not matched_in_vocab:
                    detected.add(canonical)

        return detected

    @staticmethod
    def parse_skill_list(raw_skills: str) -> List[str]:
        """Parse comma-separated or bracketed skill string into clean list."""
        if not raw_skills or not isinstance(raw_skills, str):
            return []
        cleaned = raw_skills.strip()
        if cleaned.startswith("[") and cleaned.endswith("]"):
            cleaned = cleaned[1:-1]
        parts = re.split(r"[,;]", cleaned)
        result = []
        for p in parts:
            s = p.strip().strip("'\"")
            if s and len(s) > 1:
                result.append(s)
        return result

