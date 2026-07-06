---
title: AI Resume Backend
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# 🚀 AI Resume Intelligence System

An AI-powered backend system that parses resumes and performs intelligent job matching using NLP and semantic analysis.

---

## ⚙️ Features

- 📄 Resume PDF parsing  
- 🧠 AI-based skill extraction  
- 🎯 ATS score calculation  
- 🤖 BERT-based semantic matching  
- 🔍 Job Description matching  
- 📊 Matched & missing skills detection  
- 🚀 FastAPI backend API  

---

## 🧠 Architecture Diagram

```mermaid
flowchart TD

A[Resume PDF Upload] --> B[Text Extraction]
B --> C[NLP Processing<br/>spaCy + Regex]
C --> D[Skill Extraction]
D --> E[ATS Scoring Engine]
D --> F[BERT Embedding Model]
F --> G[Semantic Job Matching]
E --> H[Final JSON Response]
G --> H

H --> I[API Response<br/>FastAPI Endpoint]
---

## 📌 API Endpoints

### POST /parse_resume
Upload resume PDF and extract structured data.

---

### POST /match_resume
Compare resume with job description.

Returns:
- ATS score  
- Match score  
- Skills comparison  

---

## 🛠 Tech Stack

Python • FastAPI • spaCy • BERT • scikit-learn • Docker  

---

## 🚀 Deployment

HuggingFace Spaces (Docker)  
Uvicorn server on port 7860  

---

## 📊 Output Example

```json
{
  "ats_score": 90,
  "match_score": 75,
  "skills": ["python", "fastapi", "nlp"]
}