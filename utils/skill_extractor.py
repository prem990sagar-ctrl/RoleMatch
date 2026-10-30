"""
Module: utils/skill_extractor.py
Purpose: Backward-compatible adapter delegating to models.skill_model.SkillModel.
"""
from typing import Set, Dict, Optional, List
import re
from models.skill_model import SkillModel, COMMON_SKILL_ALIASES


def build_skill_pattern(skill: str) -> re.Pattern:
    """Delegate to SkillModel.build_pattern."""
    return SkillModel.build_pattern(skill)


def extract_skills(
    text: str,
    dataset_skills: Optional[Set[str]] = None,
    alias_dict: Optional[Dict[str, str]] = None
) -> Set[str]:
    """Delegate skill extraction to SkillModel."""
    model = SkillModel(vocabulary=dataset_skills, alias_dict=alias_dict)
    return model.extract(text)


def normalize_skill_string(skill_raw: str) -> List[str]:
    """Delegate skill list normalization to SkillModel."""
    return SkillModel.parse_skill_list(skill_raw)
