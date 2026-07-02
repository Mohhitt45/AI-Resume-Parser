from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, job_text):

    documents = [resume_text, job_text]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return round(score * 100, 2)

def analyze_skills(resume_text, job_description):

    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    matched = sorted(list(resume_words.intersection(job_words)))
    missing = sorted(list(job_words.difference(resume_words)))

    # Chhote random words hata do
    ignore = {
        "and","or","the","to","of","for","a","an","with",
        "in","on","at","is","are","as","be","using","experience"
    }

    matched = [x for x in matched if len(x) > 2 and x not in ignore]
    missing = [x for x in missing if len(x) > 2 and x not in ignore]

    return matched, missing