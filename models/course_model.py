"""
Module: models/course_model.py
Purpose: Course catalog model and Greedy Career Path optimizer.
         Maps missing skills to high-reputation educational courses and
         builds an optimal, sequential learning path using greedy set cover.
"""
import json
import re
from pathlib import Path
from typing import List, Dict, Set, Optional, Union
from models.entities import Course, CareerPathStep

COURSES_PATH = Path(__file__).resolve().parent.parent / "data" / "courses.json"


def _skills_match(gap_skill: str, course_skill: str) -> bool:
    """Robust skill matching avoiding false positives on short symbols."""
    g = gap_skill.lower().strip()
    c = course_skill.lower().strip()
    if g == c:
        return True
    # Word boundary match for short symbols like C, R, C++
    if len(c) <= 3 or len(g) <= 3:
        pattern = r"\b" + re.escape(c) + r"\b"
        return bool(re.search(pattern, g))
    # Substring match only for longer phrases (e.g. "microservices", "machine learning")
    return g in c or c in g


class CourseModel:
    """Manages course recommendations and greedy career path construction."""

    def __init__(self, courses_path: Union[str, Path] = COURSES_PATH):
        self.courses: List[Course] = []
        self._load_courses(courses_path)

    def _load_courses(self, path: Union[str, Path]):
        courses_path = Path(path)
        if not courses_path.is_file():
            return

        with courses_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            c = Course(
                id=item.get("id", ""),
                title=item.get("title", ""),
                provider=item.get("provider", "Udemy"),
                instructor=item.get("instructor", ""),
                level=item.get("level", "Beginner"),
                duration=item.get("duration", "6w"),
                url=item.get("url", "#"),
                skills_covered=item.get("skills_covered", []),
                description=item.get("description", "")
            )
            self.courses.append(c)

    def get_courses_for_skills(self, missing_skills: List[str], max_courses: int = 2) -> List[Dict]:
        """
        Find top matching courses that cover the specified missing skills.
        Returns a list of dicts: [{"course": Course, "skill": str}]
        """
        if not missing_skills or not self.courses:
            return []

        matched_pairs = []
        seen_course_ids = set()

        for s in missing_skills:
            for c in self.courses:
                if c.id in seen_course_ids:
                    continue
                for sk in c.skills_covered:
                    if _skills_match(s, sk):
                        matched_pairs.append({
                            "course": c,
                            "skill": s
                        })
                        seen_course_ids.add(c.id)
                        break
                if len(matched_pairs) >= max_courses:
                    return matched_pairs

        return matched_pairs

    def build_greedy_career_path(self, all_gap_skills: List[str], max_steps: int = 5) -> List[CareerPathStep]:
        """
        Build a personalized career path using a greedy set-cover algorithm.
        Courses are chosen greedily to cover the most gap skills across top matched jobs,
        then ordered by difficulty (Beginner -> Intermediate -> Advanced).
        """
        if not all_gap_skills or not self.courses:
            return []

        # Clean and deduplicate gap skills
        gap_map = {s.lower().strip(): s.strip() for s in all_gap_skills if s.strip()}
        uncovered = set(gap_map.keys())

        selected_courses: List[Dict] = []
        available_courses = list(self.courses)

        while uncovered and len(selected_courses) < max_steps:
            best_course = None
            best_covered: Set[str] = set()

            for c in available_courses:
                covered_in_c = set()
                for u in uncovered:
                    for sk in c.skills_covered:
                        if _skills_match(u, sk):
                            covered_in_c.add(u)
                            break

                if len(covered_in_c) > len(best_covered):
                    best_covered = covered_in_c
                    best_course = c

            if not best_course or not best_covered:
                break

            actual_covered_names = [gap_map[u] for u in best_covered if u in gap_map]
            selected_courses.append({
                "course": best_course,
                "covered_skills": actual_covered_names
            })

            uncovered -= best_covered
            available_courses.remove(best_course)

        # Order by difficulty level
        level_order = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
        selected_courses.sort(key=lambda x: level_order.get(x["course"].level, 2))

        # Format as CareerPathStep instances
        steps = []
        for i, item in enumerate(selected_courses, start=1):
            steps.append(CareerPathStep(
                step_number=i,
                course=item["course"],
                covered_gap_skills=item["covered_skills"]
            ))

        return steps
