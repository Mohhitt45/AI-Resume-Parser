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

## 🚀 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-BERT%2FTransformers-orange?style=for-the-badge)

---

## ✨ Highlights

- 🚀 End-to-end AI Resume Parsing System
- 🧠 NLP + Transformer-based skill extraction
- ⚡ FastAPI high-performance backend
- 🐳 Dockerized deployment ready
- 📊 ATS score calculation + job matching engine
- 🔍 Modular and scalable architecture

---

## ⚙️ Features

- 📄 Resume PDF parsing  
- 🧠 AI-based skill extraction  
- 🎯 ATS score calculation  
- 🤖 BERT-based semantic matching  
- 🔍 Job description matching  
- 📊 Matched & missing skills detection  
- 🚀 FastAPI backend API  

---

## 🧠 Architecture Diagram

```mermaid
flowchart TD

A[Resume PDF Upload] --> B[Text Extraction]
B --> C["NLP Processing (spaCy + Regex)"]
C --> D[Skill Extraction]
D --> E[ATS Scoring Engine]
D --> F[BERT Embedding Model]
F --> G[Semantic Job Matching]
E --> H[Final JSON Response]
G --> H
H --> I[API Response via FastAPI]
```

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

## 🛠 Tech Stack (Detailed)

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
```