# 🚀 AI-Powered Interview Question Generator & Resume Analyzer

Hey there! Welcome to our project repository. We built this tool because let's face it—preparing for interviews and tweaking resumes can be incredibly stressful for students and job seekers. We wanted to create something genuinely useful that takes the guesswork out of the process. 

This is a Python-based recruitment assistant. You just upload your resume, paste in the job description of the role you want, and our system does the heavy lifting. It extracts your skills, compares them against the job requirements, and uses a powerful LLM (via OpenRouter/OpenAI) to generate tailored interview questions and give you actionable feedback to improve your resume's ATS score.

## 👥 The Team
This project was brought to life by:
- **Arvin Tandukar** 
- **Kashyap Subedi**
- **Angel Thapa**
- **Agrata Shrestha** (AI Integration & Prompt Engineering)

## ✨ What It Actually Does
Instead of just a basic keyword matcher, we've integrated real AI to give you meaningful insights:
- **Smart Parsing:** Upload your resume (PDF or DOCX) and paste your target job description.
- **Skill Gap Analysis:** We calculate a match percentage and tell you exactly which technical skills you're missing.
- **AI Resume Grading:** The LLM evaluates your resume and grades it as Basic, Intermediate, or Top-Tier based on the role.
- **ATS Compatibility:** Identifies formatting issues that might get you automatically rejected by standard ATS bots.
- **Tailored Interview Prep:** Generates 3 technical, 2 HR, and 2 behavioral questions specifically based on *your* background and *their* job description.
- **Actionable Feedback:** Suggests 3 specific ways to improve your resume for that exact job.

## 🛠️ Tech Stack
- **Python** (The backbone)
- **Streamlit** (For a clean, fast frontend web interface)
- **pdfplumber & python-docx** (File parsing)
- **Requests & JSON** (For talking to our AI endpoints)
- **OpenRouter / OpenAI** (Running the 120b parameter LLM for advanced NLP analysis)

## 💻 How to Run It Locally

We made sure it's super easy to spin up on your own machine. 

**1. Clone or download the folder and open it in VS Code.**

**2. Install the dependencies:**
Just run this in your terminal to grab everything you need:
```bash
pip install -r requirements.txt
```

**3. Fire it up!**
Start the Streamlit server:
```bash
streamlit run app.py
```
Your browser should automatically pop open to `http://localhost:8501`.

## 🔮 What's Next? (Future Scope)
While the core AI integration is fully functional, we're hoping to add:
- A local SQLite database to save user profiles and past analysis results.
- A PDF export feature so users can download their interview prep report.
- User authentication and login functionality.

---
*Thanks for checking out our project! We hope it helps someone land their dream job.*
