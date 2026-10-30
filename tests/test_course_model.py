"""
Unit tests for CourseModel and greedy career path construction.
"""
import pytest
from models.course_model import CourseModel
from models.entities import Course, CareerPathStep


def test_course_model_initialization():
    """Verify CourseModel loads courses from catalog."""
    model = CourseModel()
    assert len(model.courses) > 0
    sample = model.courses[0]
    assert isinstance(sample, Course)
    assert sample.title != ""
    assert sample.provider != ""
    assert len(sample.skills_covered) > 0


def test_get_courses_for_skills():
    """Verify course matching for missing skills."""
    model = CourseModel()
    results = model.get_courses_for_skills(missing_skills=["HTML", "CSS"], max_courses=2)
    assert len(results) > 0
    for r in results:
        assert "course" in r
        assert "skill" in r
        assert r["skill"] in ["HTML", "CSS"]


def test_build_greedy_career_path():
    """Verify greedy set-cover algorithm covers gap skills in difficulty order."""
    model = CourseModel()
    gap_skills = ["HTML", "JavaScript", "Spring Boot", "Microservices", "Docker"]
    steps = model.build_greedy_career_path(gap_skills, max_steps=3)

    assert len(steps) > 0
    assert len(steps) <= 3
    for i, step in enumerate(steps, start=1):
        assert isinstance(step, CareerPathStep)
        assert step.step_number == i
        assert len(step.covered_gap_skills) > 0

    # Ensure difficulty levels are ordered: Beginner <= Intermediate <= Advanced
    level_ranks = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    ranks = [level_ranks.get(s.course.level, 2) for s in steps]
    assert ranks == sorted(ranks)

