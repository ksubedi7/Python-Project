import streamlit as st
import pdfplumber
from docx import Document
import tempfile
import os
import re

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


def rate_resume(match_percentage, resume_text):
    word_count = len(resume_text.split())

    if match_percentage >= 70 and word_count >= 200:
        return "Top-Tier"
    elif match_percentage >= 40:
        return "Intermediate"
    else:
        return "Basic"


def ats_check(resume_text):
    text = resume_text.lower()
    score = 100
    issues = []

    sections = ["education", "skills", "experience", "project"]

    for section in sections:
        if section not in text:
            score -= 15
            issues.append(f"Add a clear {section.title()} section.")

    if len(resume_text.split()) < 150:
        score -= 10
        issues.append("Resume is too short. Add more details.")

    if score < 0:
        score = 0

    if not issues:
        issues.append("Resume looks ATS-friendly.")

    return score, issues


def generate_questions(resume_skills, missing_skills):
    questions = []

    questions.append("Tell me about yourself.")
    questions.append("Why are you interested in this job role?")
    questions.append("What are your strengths and weaknesses?")

    for skill in resume_skills[:5]:
        questions.append(f"Can you explain your experience with {skill}?")

    for skill in missing_skills[:3]:
        questions.append(f"This job requires {skill.title()}. How will you improve this skill?")

    questions.append("Describe one project you have worked on.")
    questions.append("Tell me about a time you worked in a team.")
    questions.append("Why should we hire you?")

    return questions


def give_suggestions(missing_skills, rating):
    suggestions = []

    if missing_skills:
        suggestions.append("Add these missing job-related skills to your resume if you have them: " + ", ".join(skill.title() for skill in missing_skills))

    if rating == "Basic":
        suggestions.append("Add more project details, technical skills, and work experience.")
        suggestions.append("Use clear headings like Education, Skills, Experience, and Projects.")

    elif rating == "Intermediate":
        suggestions.append("Your resume is decent, but it needs more job-specific keywords.")
        suggestions.append("Add measurable achievements in your project and experience sections.")

    else:
        suggestions.append("Your resume is strong. Keep it updated and customize it for every job.")

    return suggestions


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="AI Interview Generator",
    page_icon="🤖",
    layout="wide"
)

st.title("AI-Powered Interview Question Generator and Resume Analysis System")

st.markdown("""
### Project Overview
This application analyzes uploaded resumes against job descriptions,
evaluates skill compatibility, generates interview questions,
and provides resume improvement recommendations.

**Project Submitted By:** Agrata Shrestha  
**Group Members:** Arvin Tandukar, Kashyap Subedi, Angel Thapa, Agrata Shrestha

**Technology Stack:** Python, Streamlit, PDF Processing, Resume Analysis

---
""")

uploaded_file = st.file_uploader("Upload Resume PDF or DOCX", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description", height=180)

if st.button("Analyze Resume"):
    if uploaded_file is None:
        st.error("Please upload a resume.")
    elif job_description.strip() == "":
        st.error("Please paste a job description.")
    else:
        resume_text = extract_text(uploaded_file)

        if resume_text.strip() == "":
            st.error("Could not read the resume. Please try another file.")
        else:
            resume_skills = find_skills(resume_text)
            job_skills = find_skills(job_description)

            match_percentage, matched_skills, missing_skills = calculate_match(resume_skills, job_skills)
            rating = rate_resume(match_percentage, resume_text)
            ats_score, ats_issues = ats_check(resume_text)
            questions = generate_questions(resume_skills, missing_skills)
            suggestions = give_suggestions(missing_skills, rating)

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

            st.subheader("Resume Improvement Suggestions")
            for suggestion in suggestions:
                st.write("- " + suggestion)

            st.subheader("ATS Compatibility Issues")
            for issue in ats_issues:
                st.write("- " + issue)

            st.subheader("Generated Interview Questions")
            for i, question in enumerate(questions, start=1):
                st.write(f"{i}. {question}")

            with st.expander("View Extracted Resume Text"):
                st.write(resume_text)

st.markdown("---")
st.caption("AI-Powered Interview Question Generator and Resume Analysis System")
st.caption("Developed by Agrata Shrestha")