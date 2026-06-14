import streamlit as st
import pdfplumber
from docx import Document
import tempfile
import os
import re
import requests
import json

# -----------------------------
# Basic skill lists
# -----------------------------

TECHNICAL_SKILLS = [
    "python", "java", "html", "css", "javascript", "sql", "machine learning",
    "deep learning", "nlp", "data analysis", "pandas", "numpy", "flask",
    "streamlit", "django", "api", "git", "github", "sqlite", "excel",
    "communication", "teamwork", "leadership", "problem solving"
]

SOFT_SKILLS = [
    "communication", "teamwork", "leadership", "problem solving",
    "time management", "creativity", "adaptability", "presentation"
]

# -----------------------------
# AI Configuration
# -----------------------------
MODEL = "openai/gpt-oss-120b"

def call_ai(prompt, api_key):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }),
            timeout=60
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            print(f"API Error: {response.text}")
            return f"Error from AI: {response.status_code}"
    except Exception as e:
        print(f"Exception: {str(e)}")
        return f"Error connecting to AI: {str(e)}"

def extract_json_from_response(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("` \n")
        if text.lower().startswith("json"):
            text = text[4:].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Failsafe if the model returned raw text instead of JSON
        import re
        match = re.search(r'\[.*\]|\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return {}

# -----------------------------
# File reading functions
# -----------------------------

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def read_docx(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
        temp_file.write(file.read())
        temp_path = temp_file.name

    doc = Document(temp_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    os.remove(temp_path)
    return text

def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return read_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return read_docx(uploaded_file)
    else:
        return ""

# -----------------------------
# Analysis functions
# -----------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s+#.]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def find_skills(text):
    text = clean_text(text)
    found = []
    for skill in TECHNICAL_SKILLS:
        if skill in text:
            found.append(skill.title())
    return sorted(list(set(found)))

def calculate_match(resume_skills, job_skills):
    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)

    if len(job_set) == 0:
        return 0, [], []

    matched = resume_set.intersection(job_set)
    missing = job_set.difference(resume_set)

    percentage = round((len(matched) / len(job_set)) * 100, 2)
    return percentage, sorted(matched), sorted(missing)

# Agrata Shrestha's AI Integrations:
def rate_resume_ai(match_percentage, resume_text, api_key):
    prompt = f"""
You are an expert technical recruiter. Based on a skill match percentage of {match_percentage}% and the following resume text, rate the resume as EXACTLY ONE of the following: Basic, Intermediate, or Top-Tier. Return ONLY the rating word and nothing else.

Resume Text:
{resume_text[:2000]}
"""
    result = call_ai(prompt, api_key)
    if "top" in result.lower(): return "Top-Tier"
    if "inter" in result.lower(): return "Intermediate"
    return "Basic"

def ats_check_ai(resume_text, api_key):
    prompt = f"""
You are an ATS (Applicant Tracking System) expert. Analyze the following resume text for ATS compatibility. Score it out of 100 and identify up to 3 specific formatting or content issues.
Return ONLY raw JSON with keys "score" (integer) and "issues" (list of strings). Do not use markdown blocks.

Resume Text:
{resume_text[:2000]}
"""
    try:
        result = call_ai(prompt, api_key)
        data = extract_json_from_response(result)
        return int(data.get("score", 50)), data.get("issues", [])
    except:
        return 50, ["Could not analyze ATS compatibility via AI.", "Please try again later."]

def generate_questions_ai(resume_text, job_description, api_key):
    prompt = f"""
You are an expert technical interviewer. Based on the following resume and job description, generate 3 Technical interview questions, 2 HR interview questions, and 2 Behavioral interview questions.
Return ONLY a raw JSON list of strings containing all 7 questions. Do not use markdown blocks.

Resume:
{resume_text[:2000]}

Job Description:
{job_description[:1000]}
"""
    try:
        result = call_ai(prompt, api_key)
        return extract_json_from_response(result)
    except:
        return ["Could not generate AI questions.", "Please check API connection."]

def give_suggestions_ai(resume_text, job_description, api_key):
    prompt = f"""
You are a career coach. Provide 3 specific, actionable suggestions to improve the following resume for the provided job description.
Return ONLY a raw JSON list of strings containing the suggestions. Do not use markdown blocks.

Resume:
{resume_text[:2000]}

Job Description:
{job_description[:1000]}
"""
    try:
        result = call_ai(prompt, api_key)
        return extract_json_from_response(result)
    except:
        return ["Could not generate AI suggestions.", "Please check API connection."]


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="AI Interview Generator",
    page_icon="🤖",
    layout="wide"
)

# Sidebar for API Key
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input("OpenRouter API Key", type="password", help="Enter your OpenRouter API key to enable AI features.")

st.title("AI-Powered Interview Question Generator and Resume Analysis System")

st.markdown("""
### Project Overview
This application analyzes uploaded resumes against job descriptions,
evaluates skill compatibility, generates interview questions,
and provides resume improvement recommendations.

**Project Submitted By:** Agrata Shrestha  
**Group Members:** Arvin Tandukar, Kashyap Subedi, Angel Thapa, Agrata Shrestha

**Technology Stack:** Python, Streamlit, PDF Processing, Resume Analysis (Powered by OpenRouter LLM)

---
""")

uploaded_file = st.file_uploader("Upload Resume PDF or DOCX", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description", height=180)

if st.button("Analyze Resume"):
    if not api_key_input.strip():
        st.error("Please enter your OpenRouter API Key in the sidebar before analyzing.")
    elif uploaded_file is None:
        st.error("Please upload a resume.")
    elif job_description.strip() == "":
        st.error("Please paste a job description.")
    else:
        with st.spinner("Analyzing with AI... (This may take a moment)"):
            resume_text = extract_text(uploaded_file)

            if resume_text.strip() == "":
                st.error("Could not read the resume. Please try another file.")
            else:
                resume_skills = find_skills(resume_text)
                job_skills = find_skills(job_description)

                match_percentage, matched_skills, missing_skills = calculate_match(resume_skills, job_skills)
                
                # Agrata's AI Features
                rating = rate_resume_ai(match_percentage, resume_text, api_key_input.strip())
                ats_score, ats_issues = ats_check_ai(resume_text, api_key_input.strip())
                questions = generate_questions_ai(resume_text, job_description, api_key_input.strip())
                suggestions = give_suggestions_ai(resume_text, job_description, api_key_input.strip())

                st.success("Resume analysis completed.")

                st.subheader("Result Summary")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Skill Match", f"{match_percentage}%")

                with col2:
                    st.metric("Resume Rating", rating)

                with col3:
                    st.metric("ATS Score", f"{ats_score}%")

                st.subheader("Skills Found in Resume")
                st.write(resume_skills if resume_skills else "No skills found.")

                st.subheader("Skills Required by Job")
                st.write(job_skills if job_skills else "No job skills found.")

                st.subheader("Matched Skills")
                st.write([skill.title() for skill in matched_skills] if matched_skills else "No matched skills.")

                st.subheader("Missing Skills")
                st.write([skill.title() for skill in missing_skills] if missing_skills else "No missing skills.")

                st.subheader("Resume Improvement Suggestions (AI)")
                for suggestion in suggestions:
                    st.write("- " + str(suggestion))

                st.subheader("ATS Compatibility Issues (AI)")
                for issue in ats_issues:
                    st.write("- " + str(issue))

                st.subheader("Generated Interview Questions (AI)")
                for i, question in enumerate(questions, start=1):
                    st.write(f"{i}. {str(question)}")

                with st.expander("View Extracted Resume Text"):
                    st.write(resume_text)

st.markdown("---")
st.caption("AI-Powered Interview Question Generator and Resume Analysis System")
st.caption("Developed by Agrata Shrestha")