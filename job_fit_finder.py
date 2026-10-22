"""Transparent, offline role matching using explicit skill dictionaries."""
import re

ROLES = {
    "Machine Learning Engineer": ["Python", "Machine Learning", "Scikit-learn", "Pandas", "NumPy", "SQL", "TensorFlow", "Docker"],
    "Data Analyst": ["Excel", "SQL", "Python", "Pandas", "Power BI", "Statistics"],
    "Data Scientist": ["Python", "SQL", "Statistics", "Machine Learning", "Pandas", "Scikit-learn", "Data Visualization"],
    "Python Developer": ["Python", "Git", "Flask", "Django", "SQL", "REST API"],
    "AI Engineer": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "NLP", "Docker", "AWS"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Git"],
    "Backend Developer": ["Python", "SQL", "REST API", "Flask", "Docker", "Git"],
    "Cloud Engineer": ["AWS", "Docker", "Linux", "Python", "Git", "CI/CD"],
}
ALIASES = {
    "scikit-learn": ["scikit-learn", "sklearn"],
    "power bi": ["power bi", "powerbi"],
    "rest api": ["rest api", "restful api", "rest apis"],
    "ci/cd": ["ci/cd", "continuous integration"],
    "machine learning": ["machine learning", "ml models"],
    "data visualization": ["data visualization", "matplotlib", "seaborn", "plotly"],
}
def has_skill(text, skill):
    options = ALIASES.get(skill.lower(), [skill])
    return any(re.search(r"(?<![\w])" + re.escape(option) + r"(?![\w])", text, re.I)
               for option in options)

def rank_job_roles(resume_text):
    rankings = []
    for role, skills in ROLES.items():
        matched = [skill for skill in skills if has_skill(resume_text, skill)]
        missing = [skill for skill in skills if skill not in matched]
        rankings.append({
            "role": role, "score": round(len(matched) * 100 / len(skills), 1),
            "matched": matched, "missing": missing,
            "matched_count": len(matched), "total_skills": len(skills)
        })
    return sorted(rankings, key=lambda item: (-item["score"], item["role"]))
