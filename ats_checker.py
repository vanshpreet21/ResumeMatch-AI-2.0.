"""Heuristic resume checklist, not a verified ATS parsing score."""
import re

def check_ats(resume):
    text = (resume or '').lower()
    checks = {}
    tips = []
    sections = {
        'Education':r'(?im)^\s*(education|academic background|qualifications)\s*:?\s*$',
        'Skills':r'(?im)^\s*(technical skills|skills|core competencies)\s*:?\s*$',
        'Experience':r'(?im)^\s*(work experience|professional experience|experience|internships?|employment)\s*:?\s*$',
        'Projects':r'(?im)^\s*(projects|selected projects|academic projects)\s*:?\s*$'
    }
    weights = {'Education':10,'Skills':10,'Experience':10,'Projects':10,
               'Email Address':15,'Phone Number':10,'LinkedIn Profile':10,
               'Resume Length':15,'Measurable Achievements':10}
    for label,pattern in sections.items():
        checks[label] = bool(re.search(pattern,resume or ''))
        if not checks[label]: tips.append(f'Add a clearly labeled {label} section.')
    checks['Email Address'] = bool(re.search(r'[\w.+-]+@[\w.-]+\.\w+',resume or ''))
    checks['Phone Number'] = bool(re.search(r'(?<!\d)(?:\+\d{1,3}[\s-]?)?(?:\(?\d{2,5}\)?[\s-]?)?\d{5}[\s-]?\d{5}(?!\d)',resume or ''))
    checks['LinkedIn Profile'] = 'linkedin.com/' in text
    checks['Resume Length'] = 150 <= len((resume or '').split()) <= 1200
    checks['Measurable Achievements'] = bool(re.search(r'\b\d+(?:\.\d+)?\s*%',resume or ''))
    suggestions = {
        'Email Address':'Add a professional contact email.',
        'Phone Number':'Add a valid contact number.',
        'LinkedIn Profile':'Optionally include a relevant LinkedIn profile.',
        'Resume Length':'Review the resume length; prioritize relevant evidence.',
        'Measurable Achievements':'Where accurate, add specific measurable achievements.'
    }
    for key,msg in suggestions.items():
        if not checks[key]: tips.append(msg)
    return {'ats_score':sum(weights[k] for k,v in checks.items() if v),
            'checks':checks,'tips':tips}
