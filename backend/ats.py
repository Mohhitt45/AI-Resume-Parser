import re

# ----------------------------
# Known Technical Skills
# ----------------------------
KNOWN_SKILLS = {
    "python","sql","java","c++","fastapi","flask","streamlit",
    "docker","git","github","tensorflow","pytorch","scikit-learn",
    "machine learning","deep learning","nlp","bert","transformers",
    "langchain","openai","rag","faiss","postgresql","mysql",
    "power bi","tableau","excel","aws","azure","gcp",
    "linux","kubernetes","pandas","numpy","scipy"
}


def calculate_ats_score(resume_text, job_description):

    resume = resume_text.lower()
    jd = job_description.lower()

    # ----------------------------
    # Skills Score (40%)
    # ----------------------------

    jd_skills = [s for s in KNOWN_SKILLS if s in jd]

    matched = [s for s in jd_skills if s in resume]

    if len(jd_skills) == 0:
        skills_score = 0
    else:
        skills_score = (len(matched) / len(jd_skills)) * 40

    # ----------------------------
    # Experience (25%)
    # ----------------------------

    experience_words = [
        "experience",
        "worked",
        "developer",
        "engineer",
        "analyst",
        "intern"
    ]

    experience_score = 25 if any(x in resume for x in experience_words) else 0

    # ----------------------------
    # Education (15%)
    # ----------------------------

    education_words = [
        "bachelor",
        "master",
        "b.e",
        "btech",
        "m.s",
        "degree"
    ]

    education_score = 15 if any(x in resume for x in education_words) else 0

    # ----------------------------
    # Projects (10%)
    # ----------------------------

    project_words = [
        "project",
        "developed",
        "implemented",
        "built"
    ]

    project_score = 10 if any(x in resume for x in project_words) else 0

    # ----------------------------
    # Keywords (10%)
    # ----------------------------

    jd_words = set(re.findall(r"\w+", jd))
    resume_words = set(re.findall(r"\w+", resume))

    common = jd_words.intersection(resume_words)

    keyword_score = min((len(common) / 20) * 10, 10)

    total = (
        skills_score
        + experience_score
        + education_score
        + project_score
        + keyword_score
    )

    return {
        "ats_score": round(total),
        "skills_score": round(skills_score),
        "experience_score": round(experience_score),
        "education_score": round(education_score),
        "project_score": round(project_score),
        "keyword_score": round(keyword_score),
        "matched_skills": matched
    }