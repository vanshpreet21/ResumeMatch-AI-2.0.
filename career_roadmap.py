"""Practical skill-based learning plans. No external AI service required."""
from datetime import date, timedelta

SKILL_PROJECTS = {
    "python": "Build a Python CLI tool with clean functions and tests.",
    "sql": "Create a database and answer five business questions with SQL.",
    "docker": "Containerize a small Flask or FastAPI application.",
    "aws": "Deploy a demo application using an AWS free-tier eligible service; check costs first.",
    "tensorflow": "Train and evaluate a small image or text classifier.",
    "machine learning": "Compare classification models on a public dataset.",
    "flask": "Build a REST API with input validation.",
    "git": "Publish a project with meaningful commits and a README.",
    "pandas": "Clean and analyze a messy CSV dataset.",
    "numpy": "Practice numerical operations and matrix calculations.",
    "scikit-learn": "Create a preprocessing and modeling pipeline.",
    "power bi": "Build an interactive business dashboard.",
    "excel": "Create a data analysis workbook with pivot tables.",
    "react": "Build a responsive multi-page frontend.",
    "javascript": "Build an interactive website with API integration.",
}
def create_roadmap(missing_skills, weeks=4):
    skills = list(dict.fromkeys(str(s).strip() for s in missing_skills if str(s).strip()))
    if not skills:
        return []
    steps = []
    start = date.today()
    for i, skill in enumerate(skills):
        week = i % max(1, weeks) + 1
        project = SKILL_PROJECTS.get(skill.lower(), f"Build a small demonstrable project using {skill}.")
        steps.append({
            "skill": skill, "week": week,
            "goal": f"Understand core concepts of {skill} and practice with examples.",
            "project": project,
            "proof": "Add an honest project description, repository link, and what you learned.",
            "target_date": (start + timedelta(days=7 * week)).isoformat(),
        })
    return steps
