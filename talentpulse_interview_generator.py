import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field
import google.generativeai as genai
from jd_parser import JobRequirements
from resume_parser import CandidateProfile
from evaluator import CandidateEvaluation

class TechnicalQuestion(BaseModel):
    category: str = Field(description="Question focus: 'Core Skill Verification', 'Missing Gap Probe', 'System Architecture', or 'Behavioral Scenario'")
    question: str = Field(description="The specific interview question to ask")
    purpose_or_focus: str = Field(description="Why this question is included based on candidate background")
    expected_answer_key: str = Field(description="Model answer and key technical concepts the candidate should mention")
    difficulty: str = Field(description="'Easy', 'Medium', or 'Hard'")

class InterviewScript(BaseModel):
    job_title: str = Field(description="Title of the target role")
    candidate_name: str = Field(description="Name of the candidate being interviewed")
    recommended_interview_duration: str = Field(description="Suggested duration (e.g. '45 Minutes')")
    opening_icebreaker: str = Field(description="Tailored icebreaker question referencing candidate projects")
    technical_questions: List[TechnicalQuestion] = Field(description="5 targeted technical questions with answer keys")
    coding_or_practical_challenge: str = Field(description="Hands-on coding or architectural whiteboarding scenario")
    closing_evaluation_rubric: List[str] = Field(description="Checklist items for interviewer post-interview scoring")

def generate_interview_script(candidate: CandidateProfile, jd: JobRequirements, eval_results: CandidateEvaluation, api_key: str) -> InterviewScript:
    """
    Generates a tailored technical interview script and answer key based on candidate gaps,
    strengths, and job requirements.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    candidate_json = candidate.model_dump_json()
    jd_json = jd.model_dump_json()
    eval_json = eval_results.model_dump_json()
    
    prompt = f"""
You are an expert Technical Hiring Manager & Interview Generator Agent.
Construct a highly customized 5-question technical interview script with model answers for the following candidate.
Target candidate weaknesses/missing skills identified in the evaluation, while probing their reported strengths and projects.

JOB REQUIREMENTS:
\"\"\"
{jd_json}
\"\"\"

CANDIDATE PROFILE:
\"\"\"
{candidate_json}
\"\"\"

EVALUATION SUMMARY:
\"\"\"
{eval_json}
\"\"\"

Return ONLY a JSON object matching this exact structure:
{{
  "job_title": "string",
  "candidate_name": "string",
  "recommended_interview_duration": "45 Minutes",
  "opening_icebreaker": "string question",
  "technical_questions": [
    {{
      "category": "Core Skill Verification" | "Missing Gap Probe" | "System Architecture" | "Behavioral Scenario",
      "question": "string question",
      "purpose_or_focus": "string rationale",
      "expected_answer_key": "string detailed answer key",
      "difficulty": "Easy" | "Medium" | "Hard"
    }}
  ],
  "coding_or_practical_challenge": "string coding or whiteboarding challenge",
  "closing_evaluation_rubric": ["rubric item 1", "rubric item 2"]
}}
Generate exactly 5 high-quality technical questions. Do not wrap in markdown quotes if possible, or return strictly valid JSON.
"""

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    raw_json = response.text.strip()
    data = json.loads(raw_json)
    return InterviewScript(**data)
