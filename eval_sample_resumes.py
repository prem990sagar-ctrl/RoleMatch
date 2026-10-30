"""
Evaluate all 5 sample resumes end-to-end with Course Gap Matching and Greedy Career Path.
"""
import os
import json
import pandas as pd
from utils.pdf_extractor import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.recommender import JobRoleRecommender
from models.course_model import CourseModel

df = pd.read_csv("data/job_skill_set.csv")
with open("data/skills_vocabulary.json", "r", encoding="utf-8") as f:
    dataset_skills = set(json.load(f))

recommender = JobRoleRecommender(df)
course_model = CourseModel()

files = [
    ("1_software_engineer_resume.pdf", "Software Engineer (IT & Cloud)"),
    ("2_data_scientist_resume.pdf", "Data Scientist / ML Engineer (AI & Analytics)"),
    ("3_financial_analyst_resume.pdf", "Financial Analyst (Finance & Accounting)"),
    ("4_human_resources_resume.pdf", "Human Resources Specialist (HR & Talent)"),
    ("5_business_development_sales_resume.pdf", "Business Development Executive (Sales & Strategy)")
]

for fname, label in files:
    path = os.path.join("sample_resumes", fname)
    text = extract_text_from_pdf(path)
    skills = extract_skills(text, dataset_skills=dataset_skills)
    recs = recommender.recommend(text, skills, top_k=3)
    
    print(f"\n========================================================")
    print(f"RESUME: {fname} [{label}]")
    print(f"Detected skills ({len(skills)}): {sorted(list(skills))[:8]}")
    
    all_gaps = []
    for r in recs:
        courses = course_model.get_courses_for_skills(r["missing_skills"], max_courses=2)
        all_gaps.extend(r["missing_skills"])
        print(f"  #{r['rank']}: {r['job_title']} (Category: {r['category']}) | Fit: {r['overall_score']:.1f}%")
        print(f"      Matched: {r['matched_skills'][:4]}")
        print(f"      Skill gap: {r['missing_skills'][:4]}")
        if courses:
            print("      Recommended courses to close gap:")
            for item in courses:
                c = item["course"]
                print(f"        • {c.title} — {c.provider} ({c.instructor}) ({c.level}, {c.duration}) covers {item['skill']}")

    career_path = course_model.build_greedy_career_path(all_gaps, max_steps=3)
    if career_path:
        print("\n  Personalized Career Path (Greedy Set Cover):")
        for step in career_path:
            c = step.course
            print(f"    Step {step.step_number}: {c.title} ({c.provider}) - {c.level} - {c.duration} [covers: {', '.join(step.covered_gap_skills)}]")
