import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import google.generativeai as genai
from pypdf import PdfReader

class WorkExperience(BaseModel):
    company: str = Field(description="Company or organization name")
    role: str = Field(description="Job title held")
    duration: str = Field(description="Time period or years")
    highlights: List[str] = Field(description="Key achievements or responsibilities")

class CandidateProfile(BaseModel):
    candidate_name: str = Field(description="Full name of the candidate")
    email_or_contact: str = Field(description="Email or phone number if available")
    years_of_experience: float = Field(description="Total estimated years of relevant professional experience")
    technical_skills: List[str] = Field(description="Programming languages, frameworks, AI tools, databases")
    soft_skills: List[str] = Field(description="Leadership, communication, problem-solving, etc.")
    work_history: List[WorkExperience] = Field(description="List of past work experiences")
    education: List[str] = Field(description="Degrees, universities, or academic qualifications")
    projects: List[str] = Field(description="Key projects or applications built")
    certifications: List[str] = Field(description="Certifications, publications, or honors")

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts text content from an uploaded PDF file or file-like object.
    """
    reader = PdfReader(pdf_file)
    extracted_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
    return extracted_text.strip()

def parse_resume(resume_text: str, api_key: str) -> CandidateProfile:
    """
    Parses unstructured resume text into a structured CandidateProfile Pydantic model
    using Google Gemini Flash.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
You are an expert HR Resume Parser Agent.
Analyze the following candidate resume text and extract structured candidate information into strictly valid JSON format.

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

Return ONLY a JSON object matching this exact structure:
{{
  "candidate_name": "string",
  "email_or_contact": "string",
  "years_of_experience": number,
  "technical_skills": ["skill1", "skill2"],
  "soft_skills": ["soft1", "soft2"],
  "work_history": [
    {{
      "company": "string",
      "role": "string",
      "duration": "string",
      "highlights": ["highlight1", "highlight2"]
    }}
  ],
  "education": ["degree1"],
  "projects": ["project1"],
  "certifications": ["cert1"]
}}
Do not wrap in markdown quotes if possible, or return strictly valid JSON.
"""

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    raw_json = response.text.strip()
    data = json.loads(raw_json)
    return CandidateProfile(**data)

def get_sample_resume_text() -> str:
    return """
Syed Jawad UL Hassan
Email: syedjawadulhassan9@gmail.com | Phone: +92 300 1234567 | Location: Islamabad, Pakistan
GitHub: github.com/syedjawadulhassan | LinkedIn: linkedin.com/in/syedjawadulhassan

PROFESSIONAL SUMMARY:
Accomplished Senior AI Engineer with 4.5 years of experience in designing multi-agent AI platforms, RAG systems, and responsive Streamlit/Python applications. Proven expertise in LangChain, Google Gemini, Groq API, and Pydantic structured data processing.

TECHNICAL SKILLS:
- Languages: Python, SQL, JavaScript, HTML/CSS
- AI & Agentic Frameworks: LangChain, LangGraph, LlamaIndex, Google Gemini API, Groq API, Pydantic
- Vector Databases & RAG: ChromaDB, FAISS, PyPDF, Sentence-Transformers
- Web Frameworks & UI: Streamlit, FastAPI, Flask, Jinja2
- DevOps & Cloud: Git, Docker, Streamlit Cloud, GitHub Actions

PROFESSIONAL EXPERIENCE:
Lead AI Solutions Architect | GenAI Innovation Lab (2022 - Present | 2.5 Years)
- Architected enterprise RAG and multi-agent evaluation platforms serving 10,000+ monthly queries.
- Built automated classroom analysis systems (TeachTrace AI) and Socratic study coaches using LangChain and Streamlit.
- Reduced LLM latency by 40% using Groq Llama 3.3 and Gemini Flash fallback streaming.

Software Engineer - Python & Data Analytics | TechPulse Solutions (2020 - 2022 | 2 Years)
- Developed RESTful microservices with FastAPI and PostgreSQL for automated data pipelines.
- Implemented automated PDF report generators using ReportLab and Python data analytics libraries.

KEY PROJECTS:
- TeachTrace AI: Classroom diagnostic system using RAG and linguistic analysis to detect student learning gaps.
- AI Learning Coach: Socratic tutoring chatbot with dynamic roadmap tracking and weakness remediation.
- Machine Health & Efficiency Copilot: Predictive sensor anomaly model with automated financial waste auditing.

EDUCATION:
- B.S. in Computer Science | National University of Computer & Emerging Sciences (FAST-NUCES), 2020
- Certification: GenAI & Agentic AI Specialist (Pak Angels Cohort 11, 2026)
"""
