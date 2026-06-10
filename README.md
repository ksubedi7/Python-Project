# AI-Powered Interview Question Generator

## Project Overview
This is a simple Python-based interview preparation system.  
The user uploads a resume and pastes a job description. The system reads the resume, extracts basic skills, compares them with the job description, gives a skill match percentage, checks resume quality, and generates interview questions.

## Group Members
1. Arvin Tandukar
2. Kashyap Subedi
3. Angel Thapa
4. Agrata Shrestha

## Features
- Upload resume in PDF or DOCX format
- Paste job description
- Extract skills from resume
- Extract skills from job description
- Calculate skill match percentage
- Show matched and missing skills
- Rate resume as Basic, Intermediate, or Top-Tier
- Check basic ATS compatibility
- Generate interview questions
- Give resume improvement suggestions

## Technologies Used
- Python
- Streamlit
- pdfplumber
- python-docx

## How to Run

### 1. Open the folder in VS Code

### 2. Install required libraries
```bash
pip install -r requirements.txt
```

### 3. Run the project
```bash
streamlit run app.py
```

## How It Works
1. User uploads a resume.
2. User pastes a job description.
3. Python reads the resume text.
4. The system finds matching skills.
5. It calculates the match percentage.
6. It checks basic ATS compatibility.
7. It generates interview questions.

## Future Improvements
- Add Gemini or OpenAI API
- Add database to store previous results
- Add login system
- Add downloadable report
- Improve NLP skill extraction
