import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field
import google.generativeai as genai
from jd_parser import JobRequirements
from resume_parser import CandidateProfile

class CandidateEvaluation(BaseModel):
    overall_match_score: int = Field(description="Weighted overall fit score from 0 to 100")
    skills_match_score: int = Field(description="Technical & soft skills alignment score 0-100")
    experience_match_score: int = Field(description="Years & depth of experience fit score 0-100")
    education_match_score: int = Field(description="Academic background fit score 0-100")
    matching_skills: List[str] = Field(description="Technical and soft skills present in candidate that match JD")
    missing_required_skills: List[str] = Field(description="Required JD skills missing from candidate profile")
    missing_preferred_skills: List[str] = Field(description="Preferred/bonus JD skills missing from candidate profile")
    core_strengths: List[str] = Field(description="Top 3-5 key candidate strengths for this role")
    risk_factors_or_red_flags: List[str] = Field(description="Gaps, career jumps, or missing critical qualifications")
    executive_summary: str = Field(description="2-3 sentence recruiter synthesis of the candidate's fit")
    recommendation_status: str = Field(description="One of: 'Strong Match', 'Potential Match', 'Proceed with Caution', 'Not Recommended'")

def evaluate_candidate(candidate: CandidateProfile, jd: JobRequirements, api_key: str) -> CandidateEvaluation:
    """
    Evaluates candidate profile against job requirements using Google Gemini Flash,
    outputting a validated CandidateEvaluation Pydantic object.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    candidate_json = candidate.model_dump_json()
    jd_json = jd.model_dump_json()
    
    prompt = f"""
You are an expert Autonomous Candidate Evaluation Agent.
Perform a rigorous, fair, and evidence-based matching evaluation comparing the Candidate Profile against the Job Requirements.

JOB REQUIREMENTS:
\"\"\"
{jd_json}
\"\"\"

CANDIDATE PROFILE:
\"\"\"
{candidate_json}
\"\"\"

Calculate weighted scores:
- Skills Fit (45% weight)
- Experience Fit (35% weight)
- Education & Project Fit (20% weight)

Return ONLY a JSON object matching this exact structure:
{{
  "overall_match_score": number_0_to_100,
  "skills_match_score": number_0_to_100,
  "experience_match_score": number_0_to_100,
  "education_match_score": number_0_to_100,
  "matching_skills": ["skill1", "skill2"],
  "missing_required_skills": ["skill1"],
  "missing_preferred_skills": ["skill1"],
  "core_strengths": ["strength1", "strength2"],
  "risk_factors_or_red_flags": ["risk1 or none"],
  "executive_summary": "string summary",
  "recommendation_status": "Strong Match" | "Potential Match" | "Proceed with Caution" | "Not Recommended"
}}
Do not wrap in markdown quotes if possible, or return strictly valid JSON.
"""

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    raw_json = response.text.strip()
    data = json.loads(raw_json)
    return CandidateEvaluation(**data)
