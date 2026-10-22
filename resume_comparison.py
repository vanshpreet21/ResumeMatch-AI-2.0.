"""Compare two resume versions using existing analysis functions."""
def _percentage(value):
    if value is None: return 0.0
    try: return max(0.0, min(100.0, float(value)))
    except (TypeError, ValueError): return 0.0

def _summary(text, job, matcher, checker):
    result = matcher(text, job)
    ats = checker(text)
    return {
        "match_score": _percentage(result.get("match_score")),
        "ats_score": _percentage(ats.get("ats_score")),
        "skill_score": _percentage(result.get("skill_score")),
        "similarity": _percentage(result.get("similarity")),
        "matched_skills": list(result.get("matched_skills") or []),
        "missing_skills": list(result.get("missing_skills") or []),
    }

def compare_resumes(original_text, improved_text, job_description, matcher, checker):
    if not original_text.strip() or not improved_text.strip() or not job_description.strip():
        raise ValueError("Both resumes and a job description are required")
    before = _summary(original_text, job_description, matcher, checker)
    after = _summary(improved_text, job_description, matcher, checker)
    return {
        "before": before, "after": after,
        "match_delta": round(after["match_score"] - before["match_score"], 1),
        "ats_delta": round(after["ats_score"] - before["ats_score"], 1),
        "skill_delta": round(after["skill_score"] - before["skill_score"], 1),
        "new_skills": sorted(set(after["matched_skills"]) - set(before["matched_skills"])),
        "removed_skills": sorted(set(before["matched_skills"]) - set(after["matched_skills"])),
    }
