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
    job_description: str = Form("")
):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    resume_text = extract_text_from_pdf(file_path)

    # Parse resume
    parsed = parse_resume(resume_text)

    # BERT score
    score = calculate_bert_match(resume_text, job_description)

    # Skills
    matched, missing = analyze_skills(resume_text, job_description)

    # ATS score
    ats = calculate_ats_score(resume_text, job_description)

    return {
        "status": "success",
        "resume_data": parsed,
        "match_score": score,
        "ats": ats,
        "matched_skills": matched,
        "missing_skills": missing
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)