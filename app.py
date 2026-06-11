import streamlit as st

from parser.pdfparser import extract_pdf_text
from parser.docsparser import extract_docx_text

from nlp.skillextractor import extract_skills
from nlp.jdmatcher import calculate_match

st.set_page_config(
    page_title="AI Interview Coach",
    layout="wide"
)

st.title("AI Interview Coach")

# Resume Upload
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

# Job Description
job_description = st.text_area(
    "Paste Job Description",
    height=200
)

if uploaded_file:

    # Parse Resume
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_pdf_text(uploaded_file)

    else:
        resume_text = extract_docx_text(uploaded_file)

    # Resume Text
    st.subheader("Resume Content")

    st.text_area(
        "Extracted Text",
        resume_text,
        height=250
    )

    # Skills
    skills = extract_skills(resume_text)

    st.subheader("Extracted Skills")

    col1, col2, col3 = st.columns(3)

    for i, skill in enumerate(skills):

        if i % 3 == 0:
            col1.success(skill)

        elif i % 3 == 1:
            col2.success(skill)

        else:
            col3.success(skill)

    # JD Matching
    if job_description:

        match_score, missing_skills = calculate_match(
            resume_text,
            job_description
        )

        st.subheader("Match Score")

        st.progress(match_score / 100)

        st.write(f"Match Percentage: {match_score}%")

        st.subheader("Missing Skills")

        if missing_skills:

            for skill in missing_skills:
                st.error(skill)

        else:
            st.success("No missing skills detected")

        st.divider()

        # Future AI Features

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Generate Interview Questions"):
                st.info(
                    "Question Generator Coming Soon"
                )

        with col2:
            if st.button("Analyze Resume"):
                st.info(
                    "Resume Analyzer Coming Soon"
                )

        with col3:
            if st.button("Generate Learning Roadmap"):
                st.info(
                    "Roadmap Generator Coming Soon"
                )