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
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    patterns = [
        r"\+?\d{1,3}[-.\s]?\d{5}[-.\s]?\d{5}",
        r"\+?\d{1,3}[-.\s]?\d{10}",
        r"\b\d{10}\b",
        r"\b\d{5}[-.\s]\d{5}\b",
        r"\(\d{3}\)\s*\d{3}[-.\s]\d{4}"
    ]

    compact_text = re.sub(r"[^\d+]", "", text)

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return re.sub(r"[^\d+]", "", match.group())

    match = re.search(r"\d{10}", compact_text)
    if match:
        return match.group()

    return None


# -----------------------------
# LINKEDIN + GITHUB EXTRACTION
# -----------------------------
def extract_links(text):
    text = text.replace("\n", " ")

    linkedin = re.search(
        r"(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9\-_/]+",
        text
    )

    github = re.search(
        r"(https?://)?(www\.)?github\.com/[a-zA-Z0-9\-_/]+",
        text
    )

    return {
        "linkedin": linkedin.group() if linkedin else None,
        "github": github.group() if github else None
    }


# -----------------------------
# NAME EXTRACTION
# -----------------------------
def extract_name(text):
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

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
# SKILL EXTRACTION
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

    score += len(skills) * 3

    if 1000 < len(text) < 8000:
        score += 10

    keywords = ["project", "experience", "machine learning", "python", "data"]

    for k in keywords:
        if k in text.lower():
            score += 5

    return min(score, 100)


# -----------------------------
# MAIN PARSER
# -----------------------------
def parse_resume(text):
    links = extract_links(text)
    skills = extract_skills(text)

    return {
        "basic_info": {
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "linkedin": links["linkedin"],
            "github": links["github"]
        },
        "skills": skills,
        "education": extract_education(text),
        "experience_entities": extract_experience(text),
        "ats_score": calculate_ats_score(text, skills),
        "metadata": {
            "text_length": len(text)
        }
    }