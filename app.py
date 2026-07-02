from fastapi import FastAPI, UploadFile, File
import shutil

from utils import extract_text_from_pdf
from parser import parse_resume
from matcher import calculate_match_score
from bert_matcher import calculate_bert_match
from matcher import analyze_skills
from ats import calculate_ats_score

app = FastAPI()


# -----------------------------
# 1. RESUME PARSER API
# -----------------------------
@app.post("/parse_resume")
async def parse_resume_api(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)
    parsed = parse_resume(text)

    return {
        "status": "success",
        "message": "Resume parsed successfully",
        "data": parsed
    }


# -----------------------------
# 2. RESUME vs JOB MATCH API
# -----------------------------
@app.post("/match_resume")
async def match_resume(
    file: UploadFile = File(...),
    job_description: str = ""
):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from resume
    resume_text = extract_text_from_pdf(file_path)

    # Parse structured data
    parsed = parse_resume(resume_text)

    # Match score (TF-IDF cosine similarity)
    score = calculate_match_score(resume_text, job_description)

    return {
        "status": "success",
        "resume_data": parsed,
        "job_match_score": score
    }



@app.post("/match_resume_bert")
async def match_resume_bert(
    file: UploadFile = File(...),
    job_description: str = ""
):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text_from_pdf(file_path)

    parsed = parse_resume(resume_text)

    score = calculate_bert_match(resume_text, job_description)

    matched, missing = analyze_skills(
    resume_text,
    job_description
)
    ats = calculate_ats_score(
    resume_text,
    job_description
)

    return {
    "status": "success",
    "model": "BERT Semantic Matching",
    "resume_data": parsed,
    "match_score": score,
    "ats": ats,
    "matched_skills": matched,
    "missing_skills": missing
}