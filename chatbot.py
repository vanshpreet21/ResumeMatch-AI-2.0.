
# ResumeMatch AI - Career Coach Chatbot

def chatbot_response(question, result, ats):
    q = question.lower().strip()

    match = result.get("match_score", 0)
    missing = result.get("missing_skills", [])
    matched = result.get("matched_skills", [])
    ats_score = ats.get("ats_score", 0)
    tips = ats.get("tips", [])

    if any(word in q for word in [
        "missing", "lack", "skill gap", "learn"
    ]):
        if missing:
            return (
                "Your missing skills are: "
                + ", ".join(missing)
                + ".\n\nI recommend learning these skills "
                "through practical projects and adding "
                "them to your resume once demonstrated."
            )
        return "No missing skills were detected in our dictionary."

    elif any(word in q for word in [
        "ats", "format", "readability"
    ]):
        response = f"Your estimated ATS readiness is {ats_score}%."

        if tips:
            response += "\n\nSuggested improvements:\n"
            response += "\n".join(
                f"- {tip}" for tip in tips
            )

        return response

    elif any(word in q for word in [
        "match", "percentage", "score", "suitable"
    ]):
        return (
            f"Your current job match score is {match}%.\n\n"
            "This combines text similarity and skill coverage. "
            "It is not a hiring probability. "
            "Improve it by highlighting genuine, relevant "
            "skills, projects and experience."
        )

    elif any(word in q for word in [
        "strength", "good", "matched"
    ]):
        if matched:
            return (
                "Your matched skills include: "
                + ", ".join(matched)
                + ".\n\nHighlight projects where you used them."
            )
        return "No matching skills were detected."

    elif any(word in q for word in [
        "interview", "question", "prepare"
    ]):
        questions = [
            f"Explain a project where you used {skill}."
            for skill in matched[:3]
        ]

        questions.append(
            "Describe a challenging technical problem you solved."
        )

        return "Practice these questions:\n\n" + "\n".join(
            f"{i}. {item}"
            for i, item in enumerate(questions, 1)
        )

    elif any(word in q for word in [
        "improve", "suggest", "recommend", "better"
    ]):
        advice = list(tips)

        if missing:
            advice.append(
                "Develop relevant skills: " + ", ".join(missing)
            )

        if not advice:
            return (
                "Your current checks look good. "
                "Continue improving relevant project evidence."
            )

        return "My recommendations:\n\n" + "\n".join(
            f"- {tip}" for tip in advice
        )

    elif any(word in q for word in [
        "hello", "hi", "hey"
    ]):
        return (
            "Hello! I'm your ResumeMatch AI Career Coach. "
            "Ask about your ATS score, missing skills, "
            "job match or interview preparation."
        )

    return (
        "I can help you understand your resume analysis. "
        "Try asking:\n\n"
        "- How can I improve my resume?\n"
        "- What skills am I missing?\n"
        "- Why is my match score low?\n"
        "- How can I improve my ATS score?\n"
        "- Give me interview questions."
    )
