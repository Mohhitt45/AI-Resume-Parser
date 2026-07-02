from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# lightweight but powerful model
model = SentenceTransformer('all-MiniLM-L6-v2')


def calculate_bert_match(resume_text, job_text):

    # convert text → embeddings
    resume_vec = model.encode([resume_text])
    job_vec = model.encode([job_text])

    # cosine similarity
    score = cosine_similarity(resume_vec, job_vec)[0][0]

    return round(score * 100, 2)