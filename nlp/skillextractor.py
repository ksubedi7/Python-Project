def extract_skills(text):

    skills_database = [
        "python",
        "java",
        "c++",
        "sql",
        "mysql",
        "flask",
        "django",
        "streamlit",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "docker",
        "aws",
        "git",
        "github",
        "data analysis",
        "nlp"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_database:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills