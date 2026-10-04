# ⚡ TalentPulse AI — Multi-Agent Candidate Evaluation Pipeline

TalentPulse AI is an autonomous, multi-agent recruitment screening platform that converts unstructured resume PDFs and Job Descriptions (JDs) into actionable candidate evaluations, match metrics, and technical interview scripts.

## 🚀 Key Features

1. **Job Description Agent (`jd_parser.py`):** Ingests raw JD text and uses Pydantic structured output to extract required experience years, core technical skills, preferred qualifications, and key responsibilities.
2. **Resume Parser Agent (`resume_parser.py`):** Extracts raw text from PDF resumes using `PyPDF` and parses candidate work history, technical skills, education, and projects.
3. **Match & Skill Gap Evaluator Agent (`evaluator.py`):** Performs weighted scoring across skills, experience, and education; identifies matching vs. missing skills, core candidate strengths, and potential risk factors.
4. **Tailored Interview Script Agent (`interview_generator.py`):** Generates a 5-question technical interview script with model answer keys, icebreakers, and whiteboarding challenges targeted specifically at candidate skill gaps.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI Engine & Orchestration:** Google Gemini 1.5 Flash via `google-generativeai`
- **Data Validation & Parsing:** Pydantic (V2) & PyPDF

## 📦 Local Installation & Setup

1. **Clone the repository & create virtual environment:**
   ```bash
   git clone https://github.com/your-username/talentpulse-ai.git
   cd talentpulse-ai
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key:**
   Create a `.streamlit/secrets.toml` file or set environment variable:
   ```toml
   GEMINI_API_KEY = "your_google_gemini_api_key"
   ```

4. **Run Streamlit Application:**
   ```bash
   streamlit run app.py
   ```

---
*Pak Angels GenAI & Agentic AI Cohort 11 | Final Hackathon Submission*
