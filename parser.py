import spacy

nlp = spacy.load("en_core_web_sm")
import re

def extract_email(text):
    match = re.findall(r"[\w\.-]+@[\w\.-]+", text)
    return match[0] if match else None


def extract_phone(text):
    match = re.findall(r"\b\d{10}\b", text)
    return match[0] if match else None


def extract_name(text):
    doc = nlp(text)
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    
    return None

def extract_experience(text):
    doc = nlp(text)
    
    experience = []
    
    for ent in doc.ents:
        if ent.label_ in ["ORG", "DATE"]:
            experience.append(ent.text)
    
    return list(set(experience))

def extract_education(text):
    keywords = ["B.E", "B.Tech", "M.Tech", "MBA", "BSc", "MSc", "Bachelor", "Master"]
    
    found = []
    for word in keywords:
        if word.lower() in text.lower():
            found.append(word)
    
    return found


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

def calculate_ats_score(text, skills):
    score = 0

    # skills weightage
    score += len(skills) * 5

    # length check
    if 500 < len(text) < 5000:
        score += 20

    # keywords boost
    keywords = ["project", "experience", "machine learning", "python", "data"]
    for k in keywords:
        if k in text.lower():
            score += 5

    return min(score, 100)