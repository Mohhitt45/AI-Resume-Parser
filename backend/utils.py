from pdfminer.high_level import extract_text
import re


def extract_text_from_pdf(file_path):
    text = extract_text(file_path)
    return text


# -----------------------------
# EMAIL EXTRACTION
# -----------------------------
def extract_email(text):
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(pattern, text)
    return match.group() if match else None


# -----------------------------
# PHONE EXTRACTION (ROBUST)
# -----------------------------
def extract_phone(text):

    patterns = [
        r"\+?\d{1,3}[\s-]?\d{10}",              # +91 9876543210
        r"\+?\d{1,3}[\s-]?\d{5}[\s-]?\d{5}",    # +91 98765 43210
        r"\b\d{10}\b",                          # 10-digit
        r"\b\d{5}[\s-]\d{5}\b",                # 98765-43210
        r"\(\d{3}\)\s*\d{3}-\d{4}"            # (123) 456-7890
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()

    return None