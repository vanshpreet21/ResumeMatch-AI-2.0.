"""ResumeMatch: transparent skill and text matching (not a hiring prediction)."""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    'python','java','c++','javascript','html','css','react','node.js','sql','mysql',
    'mongodb','machine learning','deep learning','artificial intelligence',
    'data science','data analysis','tensorflow','pytorch','scikit-learn','pandas',
    'numpy','nlp','computer vision','opencv','flask','django','fastapi',
    'streamlit','docker','kubernetes','aws','azure','git','github','linux',
    'power bi','tableau','excel','rest api','communication','leadership',
    'problem solving','project management','data structures','algorithms',
    'distributed systems','distributed processing','knowledge graphs',
    'clustering','generative ai','accessibility','software development',
]
ALIASES = {
    'scikit-learn':['scikit-learn','sklearn'],
    'node.js':['node.js','nodejs'],
    'rest api':['rest api','restful api','rest apis'],
    'power bi':['power bi','powerbi'],
    'machine learning':['machine learning'],
    'generative ai':['generative ai','genai','generative artificial intelligence'],
    'data structures':['data structures','data structure'],
    'algorithms':['algorithms','algorithm'],
    'distributed systems':['distributed systems','distributed system'],
    'distributed processing':['distributed processing'],
    'knowledge graphs':['knowledge graphs','knowledge graph'],
    'clustering':['clustering','cluster analysis'],
    'accessibility':['accessibility','accessible technology'],
}

def normalize_text(text):
    return re.sub(r'\s+', ' ', (text or '').lower()).strip()

def extract_skills(text):
    text = normalize_text(text)
    found = []
    for skill in SKILLS:
        alternatives = ALIASES.get(skill, [skill])
        if any(re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', text) for term in alternatives):
            found.append(skill)
    return sorted(set(found))

def calculate_similarity(resume, jd):
    if not (resume or '').strip() or not (jd or '').strip():
        return 0.0
    try:
        vectors = TfidfVectorizer(stop_words='english', ngram_range=(1,2)).fit_transform([resume,jd])
        return round(float(cosine_similarity(vectors[0:1],vectors[1:2])[0][0])*100,2)
    except ValueError:
        return 0.0

def analyze_resume(resume, jd):
    similarity = calculate_similarity(resume, jd)
    resume_skills, job_skills = set(extract_skills(resume)), set(extract_skills(jd))
    matched, missing = sorted(resume_skills & job_skills), sorted(job_skills-resume_skills)
    skill_score = round(100*len(matched)/len(job_skills),2) if job_skills else None
    match_score = round(0.6*similarity + 0.4*skill_score,2) if skill_score is not None else similarity
    return dict(similarity=similarity,match_score=match_score,skill_score=skill_score,
                matched_skills=matched,missing_skills=missing,
                resume_skills=sorted(resume_skills),job_skills=sorted(job_skills))
