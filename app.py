import logging
from fastapi import FastAPI, UploadFile, File
import shutil

from utils import extract_text_from_pdf
from parser import parse_resume

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/parse_resume")
async def parse_resume_api(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    logger.info(f"Resume uploaded: {file.filename}")

    text = extract_text_from_pdf(file_path)
    logger.info("PDF text extracted successfully")
    result = parse_resume(text)
    logger.info("Resume parsed successfully")

    return {
    "status": "success",
    "message": "Resume parsed successfully",
    "data": result
}