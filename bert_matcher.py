from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

def calculate_bert_match(resume_text, job_text):
    model = get_model()

    resume_vec = model.encode([resume_text])
    job_vec = model.encode([job_text])

    score = cosine_similarity(resume_vec, job_vec)[0][0]
    return round(score * 100, 2)