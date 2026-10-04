import os
import json
import streamlit as st
from pypdf import PdfReader

from jd_parser import parse_job_description, get_sample_jd, JobRequirements
from resume_parser import parse_resume, extract_text_from_pdf, get_sample_resume_text, CandidateProfile
from evaluator import evaluate_candidate, CandidateEvaluation
from interview_generator import generate_interview_script, InterviewScript

# Page Configuration
st.set_page_config(
    page_title="TalentPulse AI | Autonomous Recruitment Pipeline",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .badge-primary {
        background-color: #EEF2FF;
        color: #4F46E5;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .badge-success {
        background-color: #ECFDF5;
        color: #059669;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .badge-danger {
        background-color: #FEF2F2;
        color: #DC2626;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .badge-warning {
        background-color: #FFFBEB;
        color: #D97706;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "")
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "jd_data" not in st.session_state:
    st.session_state.jd_data = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = None
if "eval_data" not in st.session_state:
    st.session_state.eval_data = None
if "script_data" not in st.session_state:
    st.session_state.script_data = None

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/sparkling.png", width=64)
    st.title("TalentPulse AI")
    st.caption("Multi-Agent Candidate Evaluation Pipeline")
    st.markdown("---")
    
    # API Key Management
    user_api_key = st.text_input(
        "Google Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        help="Get a free key from Google AI Studio (aistudio.google.com)"
    )
    if user_api_key:
        st.session_state.api_key = user_api_key
        
    st.markdown("---")
    st.subheader("📌 Pipeline Status")
    st.write(f"• **Job Description:** {'✅ Parsed' if st.session_state.jd_data else '⏳ Pending'}")
    st.write(f"• **Candidate Resume:** {'✅ Parsed' if st.session_state.candidate_data else '⏳ Pending'}")
    st.write(f"• **Evaluation Score:** {'✅ Generated' if st.session_state.eval_data else '⏳ Pending'}")
    st.write(f"• **Interview Script:** {'✅ Generated' if st.session_state.script_data else '⏳ Pending'}")
    
    st.markdown("---")
    st.caption("Pak Angels GenAI Cohort 11 Final Hackathon")

# Main Title Header
st.markdown('<div class="main-header">⚡ TalentPulse AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Autonomous multi-agent candidate evaluation, skill gap analysis & interview script generator</div>', unsafe_allow_html=True)

if not st.session_state.api_key:
    st.warning("⚠️ Please enter your Google Gemini API Key in the sidebar to run the multi-agent pipeline.")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Job Description (JD Agent)",
    "2️⃣ Resume Parser Agent",
    "3️⃣ Match & Gap Evaluator Agent",
    "4️⃣ Tailored Interview Script Agent"
])

# ---------------------------------------------------------
# TAB 1: JOB DESCRIPTION PARSER
# ---------------------------------------------------------
with tab1:
    st.header("📄 Step 1: Job Description Ingestion")
    st.write("Input the target Job Description to extract structured requirements using the JD Agent.")
    
    col_jd_left, col_jd_right = st.columns([1.2, 1])
    
    with col_jd_left:
        btn_sample_jd = st.button("📋 Load Sample JD (Senior AI Engineer)")
        if btn_sample_jd:
            st.session_state.jd_text = get_sample_jd()
            
        jd_input = st.text_area(
            "Paste Job Description Text",
            value=st.session_state.jd_text,
            height=320,
            placeholder="Paste full Job Description text here..."
        )
        st.session_state.jd_text = jd_input
        
        btn_parse_jd = st.button("🚀 Run JD Parser Agent", type="primary", use_container_width=True)
        if btn_parse_jd:
            if not st.session_state.api_key:
                st.error("Please provide a valid Gemini API key in the sidebar.")
            elif not jd_input.strip():
                st.error("Please paste a Job Description before running the parser.")
            else:
                with st.spinner("JD Agent is extracting structured requirements..."):
                    try:
                        jd_obj = parse_job_description(jd_input, st.session_state.api_key)
                        st.session_state.jd_data = jd_obj
                        st.success("✅ Job Description parsed successfully!")
                    except Exception as e:
                        st.error(f"Error parsing JD: {e}")

    with col_jd_right:
        st.subheader("🎯 Extracted Requirements")
        if st.session_state.jd_data:
            jd = st.session_state.jd_data
            st.markdown(f"### {jd.job_title}")
            st.write(f"**Experience Required:** `{jd.experience_years_required} Years` | **Education:** `{jd.education_level}`")
            
            st.markdown("#### Required Technical Skills")
            for skill in jd.required_technical_skills:
                st.markdown(f'<span class="badge-primary">{skill}</span>', unsafe_allow_html=True)
                
            st.markdown("#### Preferred / Bonus Skills")
            for skill in jd.preferred_skills:
                st.markdown(f'<span class="badge-success">{skill}</span>', unsafe_allow_html=True)
                
            st.markdown("#### Core Responsibilities")
            for resp in jd.core_responsibilities:
                st.write(f"• {resp}")
        else:
            st.info("Parsed job requirements will appear here once you run the JD Agent.")

# ---------------------------------------------------------
# TAB 2: RESUME PARSER AGENT
# ---------------------------------------------------------
with tab2:
    st.header("📝 Step 2: Resume Extraction & Profiling")
    st.write("Upload a candidate PDF resume or load sample candidate text.")
    
    col_res_left, col_res_right = st.columns([1.2, 1])
    
    with col_res_left:
        btn_sample_res = st.button("👤 Load Sample Resume (Syed Jawad UL Hassan)")
        if btn_sample_res:
            st.session_state.resume_text = get_sample_resume_text()
            
        uploaded_pdf = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        if uploaded_pdf is not None:
            try:
                extracted_pdf_text = extract_text_from_pdf(uploaded_pdf)
                st.session_state.resume_text = extracted_pdf_text
                st.success(f"PDF uploaded: {uploaded_pdf.name} ({len(extracted_pdf_text)} characters extracted)")
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
                
        resume_input = st.text_area(
            "Candidate Resume Raw Text",
            value=st.session_state.resume_text,
            height=250,
            placeholder="Resume text extracted from PDF or pasted directly..."
        )
        st.session_state.resume_text = resume_input
        
        btn_parse_resume = st.button("🚀 Run Resume Parser Agent", type="primary", use_container_width=True)
        if btn_parse_resume:
            if not st.session_state.api_key:
                st.error("Please provide a valid Gemini API key in the sidebar.")
            elif not resume_input.strip():
                st.error("Please upload or paste a candidate resume before running the parser.")
            else:
                with st.spinner("Resume Agent is extracting candidate profile..."):
                    try:
                        candidate_obj = parse_resume(resume_input, st.session_state.api_key)
                        st.session_state.candidate_data = candidate_obj
                        st.success("✅ Candidate Resume parsed successfully!")
                    except Exception as e:
                        st.error(f"Error parsing resume: {e}")

    with col_res_right:
        st.subheader("👤 Parsed Candidate Profile")
        if st.session_state.candidate_data:
            c = st.session_state.candidate_data
            st.markdown(f"### {c.candidate_name}")
            st.write(f"**Contact:** `{c.email_or_contact}`")
            st.write(f"**Experience:** `{c.years_of_experience} Years` | **Education:** `{', '.join(c.education)}`")
            
            st.markdown("#### Technical Skills")
            for skill in c.technical_skills:
                st.markdown(f'<span class="badge-primary">{skill}</span>', unsafe_allow_html=True)
                
            st.markdown("#### Work History")
            for job in c.work_history:
                st.write(f"**{job.role}** at `{job.company}` ({job.duration})")
                for h in job.highlights[:2]:
                    st.caption(f"  • {h}")
                    
            st.markdown("#### Projects")
            for proj in c.projects:
                st.write(f"• {proj}")
        else:
            st.info("Parsed candidate profile will appear here once you run the Resume Agent.")

# ---------------------------------------------------------
# TAB 3: MATCH & GAP EVALUATOR AGENT
# ---------------------------------------------------------
with tab3:
    st.header("📊 Step 3: Match & Skill Gap Evaluation")
    st.write("Run the Evaluator Agent to perform weighted scoring, gap analysis, and risk assessment.")
    
    if not st.session_state.jd_data or not st.session_state.candidate_data:
        st.warning("⚠️ Please complete Step 1 (JD Agent) and Step 2 (Resume Agent) before running the Evaluation Agent.")
    else:
        btn_run_eval = st.button("⚖️ Run Candidate Evaluation Agent", type="primary")
        if btn_run_eval:
            with st.spinner("Evaluator Agent is performing multi-factor matching & gap analysis..."):
                try:
                    eval_obj = evaluate_candidate(
                        st.session_state.candidate_data,
                        st.session_state.jd_data,
                        st.session_state.api_key
                    )
                    st.session_state.eval_data = eval_obj
                    st.success("✅ Candidate evaluation complete!")
                except Exception as e:
                    st.error(f"Error during evaluation: {e}")
                    
        if st.session_state.eval_data:
            ev = st.session_state.eval_data
            
            st.markdown("---")
            # Executive Header Cards
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Overall Match Score", f"{ev.overall_match_score}%")
            with m2:
                st.metric("Skills Alignment", f"{ev.skills_match_score}%")
            with m3:
                st.metric("Experience Alignment", f"{ev.experience_match_score}%")
            with m4:
                status_color = "badge-success" if "Strong" in ev.recommendation_status else ("badge-warning" if "Potential" in ev.recommendation_status else "badge-danger")
                st.markdown(f"**Recommendation:**<br><span class='{status_color}' style='font-size:1.1rem;'>{ev.recommendation_status}</span>", unsafe_allow_html=True)
                
            st.progress(ev.overall_match_score / 100.0)
            
            st.markdown("### Executive Summary")
            st.info(ev.executive_summary)
            
            col_gap1, col_gap2, col_gap3 = st.columns(3)
            with col_gap1:
                st.markdown("#### ✅ Matching Skills")
                for s in ev.matching_skills:
                    st.markdown(f'<span class="badge-success">✓ {s}</span>', unsafe_allow_html=True)
            with col_gap2:
                st.markdown("#### ❌ Missing Required Skills")
                if ev.missing_required_skills:
                    for s in ev.missing_required_skills:
                        st.markdown(f'<span class="badge-danger">✗ {s}</span>', unsafe_allow_html=True)
                else:
                    st.caption("No required skills missing!")
            with col_gap3:
                st.markdown("#### ⚠️ Missing Preferred Skills")
                if ev.missing_preferred_skills:
                    for s in ev.missing_preferred_skills:
                        st.markdown(f'<span class="badge-warning">! {s}</span>', unsafe_allow_html=True)
                else:
                    st.caption("All preferred skills present!")
                    
            st.markdown("---")
            c_str, c_risk = st.columns(2)
            with c_str:
                st.markdown("#### 🌟 Core Strengths")
                for st_item in ev.core_strengths:
                    st.write(f"• {st_item}")
            with c_risk:
                st.markdown("#### ⚠️ Risk Factors / Gap Probes")
                for r_item in ev.risk_factors_or_red_flags:
                    st.write(f"• {r_item}")

# ---------------------------------------------------------
# TAB 4: TAILORED TECHNICAL INTERVIEW SCRIPT AGENT
# ---------------------------------------------------------
with tab4:
    st.header("🎙️ Step 4: Customized Technical Interview Script")
    st.write("Generate a 5-question targeted technical interview guide with model answer keys tailored specifically to this candidate.")
    
    if not st.session_state.eval_data:
        st.warning("⚠️ Please complete Step 3 (Candidate Evaluation) before generating the technical interview script.")
    else:
        btn_gen_script = st.button("⚡ Generate Technical Interview Script", type="primary")
        if btn_gen_script:
            with st.spinner("Interview Generator Agent is constructing targeted questions & answer keys..."):
                try:
                    script_obj = generate_interview_script(
                        st.session_state.candidate_data,
                        st.session_state.jd_data,
                        st.session_state.eval_data,
                        st.session_state.api_key
                    )
                    st.session_state.script_data = script_obj
                    st.success("✅ Technical interview script generated successfully!")
                except Exception as e:
                    st.error(f"Error generating interview script: {e}")
                    
        if st.session_state.script_data:
            scr = st.session_state.script_data
            
            st.markdown("---")
            st.subheader(f"Technical Interview Guide for {scr.candidate_name}")
            st.write(f"**Target Position:** `{scr.job_title}` | **Recommended Duration:** `{scr.recommended_interview_duration}`")
            
            st.markdown("#### 🧊 Icebreaker Opening Question")
            st.info(scr.opening_icebreaker)
            
            st.markdown("#### 🎯 Targeted Technical Questions & Expected Answer Keys")
            for idx, q in enumerate(scr.technical_questions, 1):
                diff_class = "badge-success" if q.difficulty == "Easy" else ("badge-warning" if q.difficulty == "Medium" else "badge-danger")
                with st.expander(f"Q{idx} [{q.category}] — {q.question}"):
                    st.markdown(f"**Category:** `{q.category}` | **Difficulty:** <span class='{diff_class}'>{q.difficulty}</span>", unsafe_allow_html=True)
                    st.write(f"**Question Rationale:** *{q.purpose_or_focus}*")
                    st.markdown("##### 🔑 Expected Model Answer & Key Concepts:")
                    st.success(q.expected_answer_key)
                    
            st.markdown("#### 💻 Practical Coding / Whiteboarding Challenge")
            st.code(scr.coding_or_practical_challenge, language="python")
            
            st.markdown("#### 📝 Post-Interview Evaluation Rubric")
            for r_item in scr.closing_evaluation_rubric:
                st.checkbox(r_item)
                
            # Export Option
            st.markdown("---")
            markdown_export = f"""# TalentPulse AI — Candidate Evaluation & Interview Script
Candidate Name: {scr.candidate_name}
Target Role: {scr.job_title}
Overall Match Score: {st.session_state.eval_data.overall_match_score}%
Recommendation: {st.session_state.eval_data.recommendation_status}

## Executive Summary
{st.session_state.eval_data.executive_summary}

## Interview Script
### Icebreaker:
{scr.opening_icebreaker}

### Questions:
"""
            for i, q in enumerate(scr.technical_questions, 1):
                markdown_export += f"\nQ{i} ({q.category} - {q.difficulty}): {q.question}\nAnswer Key: {q.expected_answer_key}\n"
                
            st.download_button(
                label="📥 Download Candidate Evaluation Report (Markdown)",
                data=markdown_export,
                file_name=f"{scr.candidate_name.replace(' ', '_')}_TalentPulse_Evaluation.md",
                mime="text/markdown"
            )
