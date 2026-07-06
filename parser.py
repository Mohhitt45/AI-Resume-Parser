import spacy
import re

nlp = spacy.load("en_core_web_sm")


# -----------------------------
# EMAIL EXTRACTION
# -----------------------------
def extract_email(text):
    match = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match[0] if match else None


# -----------------------------
# PHONE EXTRACTION (ROBUST)
# -----------------------------
def extract_phone(text):
    patterns = [
        r"\+?\d{1,3}[\s-]?\d{10}",              # +91 9876543210
        r"\+?\d{1,3}[\s-]?\d{5}[\s-]?\d{5}",    # +91 98765 43210
        r"\b\d{10}\b",                          # 10-digit
        r"\b\d{5}[\s-]\d{5}\b",                # 98765-43210
        r"\(\d{3}\)\s*\d{3}-\d{4}"            # (123) 456-7890
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()

    return None


# -----------------------------
# NAME EXTRACTION (IMPROVED)
# -----------------------------
def extract_name(text):
    doc = nlp(text)

    # 1. spaCy PERSON entity
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    # 2. fallback heuristic (first meaningful line)
    lines = text.split("\n")
    for line in lines[:5]:
        line = line.strip()
        if 2 <= len(line.split()) <= 4 and line.replace(" ", "").isalpha():
            return line

    return None


# -----------------------------
# EXPERIENCE EXTRACTION
# -----------------------------
def extract_experience(text):
    doc = nlp(text)

    experience = []
    for ent in doc.ents:
        if ent.label_ in ["ORG", "DATE"]:
            experience.append(ent.text)

    return list(set(experience))


# -----------------------------
# EDUCATION EXTRACTION
# -----------------------------
def extract_education(text):
    keywords = [
        "B.E", "B.Tech", "M.Tech", "MBA",
        "BSc", "MSc", "Bachelor", "Master"
    ]

    found = []
    text_lower = text.lower()

    for word in keywords:
        if word.lower() in text_lower:
            found.append(word)

    return found


# -----------------------------
# SKILL EXTRACTION (STATIC DB)
# -----------------------------
def extract_skills(text):
    skills_db = [
        "python", "sql", "machine learning", "deep learning",
        "nlp", "fastapi", "docker", "power bi",
        "llm", "langchain", "bert", "rag", "pytorch"
    ]

    text_lower = text.lower()

    found = []
    for skill in skills_db:
        if skill in text_lower:
            found.append(skill)

    return list(set(found))


# -----------------------------
# ATS SCORE
# -----------------------------
def calculate_ats_score(text, skills):
    score = 0

    # skills weightage
    score += len(skills) * 5

    # length check
    if 500 < len(text) < 5000:
        score += 20

    # keyword boost
    keywords = ["project", "experience", "machine learning", "python", "data"]

    for k in keywords:
        if k in text.lower():
            score += 5

    return min(score, 100)


# -----------------------------
# MAIN PARSER
# -----------------------------
def parse_resume(text):
    skills = extract_skills(text)

    return {
        "basic_info": {
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text)
        },
        "skills": skills,
        "education": extract_education(text),
        "experience_entities": extract_experience(text),
        "ats_score": calculate_ats_score(text, skills),
        "metadata": {
            "text_length": len(text)
        }
    }