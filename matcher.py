from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# SMART SKILL DICTIONARY
# -----------------------------
SKILL_ALIASES = {
    "python": ["python"],
    "sql": ["sql"],
    "fastapi": ["fastapi"],
    "docker": ["docker"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "artificial intelligence": ["ai", "artificial intelligence"],
    "llm": ["llm", "large language model", "large language models"],
    "rag": ["rag", "retrieval augmented generation"],
    "bert": ["bert"],
    "nlp": ["nlp"],
    "power bi": ["power bi", "powerbi"],
    "pytorch": ["pytorch"],
    "tensorflow": ["tensorflow"],
    "langchain": ["langchain"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "aws": ["aws"],
    "azure": ["azure"],
    "git": ["git"]
}


IGNORE_WORDS = {
    "and","or","the","to","of","for","a","an","with",
    "in","on","at","is","are","as","be","using","experience",
    "engineer","developer","worked","working","project"
}


# -----------------------------
# 1. SEMANTIC MATCH SCORE
# -----------------------------
def calculate_match_score(resume_text, job_text):

    documents = [resume_text, job_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return round(score * 100, 2)


# -----------------------------
# 2. SMART SKILL MATCHING
# -----------------------------
def analyze_skills(resume_text, job_description):

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    matched = []
    missing = []

    for skill, aliases in SKILL_ALIASES.items():

        resume_found = any(a in resume_text for a in aliases)
        job_found = any(a in job_description for a in aliases)

        if resume_found and job_found:
            matched.append(skill)

        elif job_found:
            missing.append(skill)

    return sorted(set(matched)), sorted(set(missing))