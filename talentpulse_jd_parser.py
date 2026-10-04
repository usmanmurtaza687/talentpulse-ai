import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field
import google.generativeai as genai

class JobRequirements(BaseModel):
    job_title: str = Field(description="Title of the position")
    experience_years_required: float = Field(description="Minimum required years of professional experience")
    required_technical_skills: List[str] = Field(description="Must-have technical skills, frameworks, languages")
    preferred_skills: List[str] = Field(description="Nice-to-have or bonus skills")
    core_responsibilities: List[str] = Field(description="Key day-to-day responsibilities")
    education_level: str = Field(description="Required education degree or equivalent experience")

def parse_job_description(jd_text: str, api_key: str) -> JobRequirements:
    """
    Parses unstructured Job Description text into a structured JobRequirements Pydantic model
    using Google Gemini Flash.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
You are an expert HR Technical Recruiter Agent.
Analyze the following Job Description (JD) and extract the structured information in strictly valid JSON format.

JOB DESCRIPTION TEXT:
\"\"\"
{jd_text}
\"\"\"

Return ONLY a JSON object matching this exact structure:
{{
  "job_title": "string",
  "experience_years_required": number,
  "required_technical_skills": ["skill1", "skill2"],
  "preferred_skills": ["bonus1", "bonus2"],
  "core_responsibilities": ["resp1", "resp2"],
  "education_level": "string"
}}
Do not wrap in markdown quotes if possible, or return strictly valid JSON.
"""
    
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    raw_json = response.text.strip()
    data = json.loads(raw_json)
    return JobRequirements(**data)

def get_sample_jd() -> str:
    return """
Senior Full-Stack AI Engineer
Location: Remote / Hybrid
Experience Required: 4+ Years

About the Role:
We are seeking a Senior Full-Stack AI Engineer to build and scale multi-agent GenAI applications and enterprise RAG solutions. You will work directly with LLM orchestration frameworks, vector databases, and responsive Streamlit/React web interfaces.

Key Responsibilities:
- Design, build, and deploy agentic AI pipelines using LangChain, LangGraph, and Google Gemini / Groq APIs.
- Architect high-speed document ingestion pipelines using PyPDF, Pydantic, and ChromaDB / FAISS vector stores.
- Develop interactive, production-grade frontend interfaces in Python Streamlit.
- Optimize LLM latency, token usage, and prompt safety guardrails.
- Collaborate with product teams to translate complex business workflows into automated AI applications.

Required Qualifications & Skills:
- 4+ years of hands-on experience in Python backend development and AI orchestration.
- Deep expertise with LangChain, LlamaIndex, or LangGraph.
- Proficient with Google Gemini, OpenAI, or Groq API integrations.
- Strong experience in vector databases (ChromaDB, FAISS, Pinecone).
- Demonstrated experience in Streamlit, FastAPI, or Flask web application development.
- Solid understanding of Pydantic data validation and structured JSON extraction.
- Bachelor's degree in Computer Science, Software Engineering, or related technical field.

Preferred / Bonus Skills:
- Experience with multi-agent orchestration frameworks (CrewAI, AutoGen).
- Knowledge of Docker, GitHub Actions, and Streamlit Cloud deployment pipelines.
- Familiarity with CI/CD and automated LLM evaluation frameworks.
"""
