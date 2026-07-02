import re

def extract_email(text):
    match = re.findall(r"[\w\.-]+@[\w\.-]+", text)
    return match[0] if match else None


def extract_phone(text):
    match = re.findall(r"\b\d{10}\b", text)
    return match[0] if match else None


def extract_name(text):
    lines = text.split("\n")
    
    for line in lines[:10]:
        line = line.strip()
        
        # ignore emails, headers, random text
        if len(line) > 2 and len(line) < 50:
            if "@" not in line and not any(char.isdigit() for char in line):
                return line
                
    return None


def extract_skills(text):
    skills_db = [
        "python", "sql", "machine learning", "deep learning",
        "nlp", "pandas", "numpy", "tensorflow", "pytorch",
        "fastapi", "docker", "power bi", "tableau",
        "llm", "langchain", "bert", "rag"
    ]

    text = text.lower()
    
    found = []
    
    for skill in skills_db:
        if skill in text:
            found.append(skill.upper())
    
    return list(set(found))


def parse_resume(text):
    return {
        "status": "success",
        "extracted_data": {
            "basic_info": {
                "name": extract_name(text),
                "email": extract_email(text),
                "phone": extract_phone(text)
            },
            "skills": extract_skills(text)
        },
        "metadata": {
            "text_length": len(text)
        }
    }