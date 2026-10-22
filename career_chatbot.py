"""Offline, explainable career coach based on the latest computed analysis."""
import re

def _list(items, limit=8):
    items = [str(x) for x in (items or [])]
    return ", ".join(items[:limit]) + (" and more" if len(items) > limit else "") if items else "none detected"

def coach_reply(question, result, ats, job_description=""):
    q = re.sub(r"\s+", " ", question.lower()).strip()
    if not q:
        return "Ask about your job match, ATS checklist, skill gaps, projects, interview preparation or learning roadmap."
    match = float(result.get("match_score") or 0)
    skill = result.get("skill_score")
    similarity = float(result.get("similarity") or 0)
    ats_score = float(ats.get("ats_score") or 0)
    matched = result.get("matched_skills") or []
    missing = result.get("missing_skills") or []
    tips = ats.get("tips") or []
    checks = ats.get("checks") or {}
    if any(w in q for w in ["hello", "hi", "hey", "help", "what can you do"]):
        return "I can explain your match and ATS scores, list detected skills, suggest honest resume improvements, propose projects, and help you prepare for interviews. I work offline using your analysis results."
    if any(w in q for w in ["guarantee", "get hired", "will i get", "selected", "offer"]):
        return "No resume tool can guarantee selection. These are estimated scores from a keyword and text-similarity model, not a hiring decision. Focus on demonstrated skills, relevant projects and interview preparation."
    if any(w in q for w in ["missing", "gap", "lack", "need to learn", "what should i learn", "learn first"]):
        if not missing:
            return "The current skill dictionary did not detect missing job skills. This does not mean you meet every requirement. Review the full job description as well."
        return "Detected gaps: **" + _list(missing) + "**. Start with **" + str(missing[0]) + "**, practice the fundamentals, build a small project, and document only skills you can demonstrate. Open Career Roadmap for weekly milestones."
    if any(w in q for w in ["matched", "existing skills", "strength", "what skills do i have"]):
        return "Skills detected in both your resume and the job description: **" + _list(matched) + "**. Be ready to describe a real example for each one."
    if any(w in q for w in ["ats", "format", "checklist"]):
        failed = [str(k) for k,v in checks.items() if not v]
        return (f"Your custom ATS-readiness checklist score is **{ats_score:.1f}%** (not an official ATS score). "
                + ("Checks to review: **" + _list(failed) + "**. " if failed else "All current checklist items passed. ")
                + ("Suggestions: " + "; ".join(map(str,tips[:3])) if tips else "Keep the resume accurate and readable."))
    if any(w in q for w in ["match", "score", "percentage", "fit", "similarity"]):
        detail = f"Skill coverage: **{float(skill):.1f}%**. " if skill is not None else "Skill coverage is unavailable for this job description. "
        return f"Estimated job match: **{match:.1f}%**. Text similarity: **{similarity:.1f}%**. " + detail + f"ATS checklist: **{ats_score:.1f}%**. These are model estimates, not recruitment outcomes."
    if any(w in q for w in ["interview", "question", "prepare"]):
        topic = str((matched or missing or ["a project"])[0])
        return f"Try these questions: 1. Describe a project where you used {topic}. 2. Explain a technical challenge and how you solved it. 3. How would you approach a task involving {str((missing or [topic])[0])}? Open Mock Interview to practice and receive heuristic feedback."
    if any(w in q for w in ["project", "portfolio"]):
        topic = str((missing or matched or ["Python"])[0])
        return f"A useful project could demonstrate **{topic}** in a practical application. Include the problem, your contribution, code repository, tests, and honest measurable outcomes. Don't claim experience you haven't gained."
    if any(w in q for w in ["improve", "rewrite", "resume", "recommend", "suggest"]):
        pieces = ["Use clear headings, accurate dates, concise achievement bullets and evidence of your work."]
        if missing: pieces.append("Prioritize learning: " + _list(missing[:3]) + ".")
        if tips: pieces.append("Checklist suggestions: " + "; ".join(map(str,tips[:3])) + ".")
        return " ".join(pieces) + " Never add unearned skills or fabricated achievements."
    if any(w in q for w in ["roadmap", "plan", "week"]):
        return "Open **Career Roadmap** in the sidebar for skill-specific milestones, practice projects and progress tracking. Your current detected gaps are: " + _list(missing) + "."
    return "I can answer questions about your job match, matched/missing skills, ATS checklist, resume improvements, project ideas, mock interviews, and learning roadmap. Try asking: 'What are my missing skills?' This coach is offline and rule-based, not a generative LLM."
