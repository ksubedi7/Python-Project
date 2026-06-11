from docx import Document

def extract_docx_text(docx_file):

    doc = Document(docx_file)

    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text