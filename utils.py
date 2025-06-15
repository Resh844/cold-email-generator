# app/utils.py
import docx
import pdfplumber
from io import BytesIO
import re

def extract_text_from_pdf(pdf_bytes):
    try:
        text = ""
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception:
        return "Error reading PDF file. Please upload a valid resume."

def extract_text_from_docx(docx_bytes):
    doc = docx.Document(BytesIO(docx_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_resume_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file.read())
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file.read())
    else:
        return "Unsupported file format."

def extract_skills_projects(resume_text):
    skills = []
    projects = []
    lines = resume_text.splitlines()
    for line in lines:
        line = line.strip()
        if "project" in line.lower():
            projects.append(line)
        if any(keyword in line.lower() for keyword in ["skill", "technologies", "tools","project", "developed", "built", "created", "implemented"]):
            skills.append(line)
    return {
        "skills": " | ".join(skills) if skills else "Not found",
        "projects": "\n".join(projects) if projects else "Not found"
    }

def extract_keywords_from_job_description(description):
    words = re.findall(r'\b\w+\b', description.lower())
    common_words = {"and", "the", "with", "you", "for", "are", "our", "your", "this", "that"}
    keywords = list(set(word for word in words if word not in common_words and len(word) > 3))
    return keywords

def match_resume_keywords(resume_text, keywords):
    matched = []
    missing = []
    lower_resume = resume_text.lower()
    for keyword in keywords:
        if keyword in lower_resume:
            matched.append(keyword)
        else:
            missing.append(keyword)
    return matched, missing


def is_valid_url(url):
    import re
    pattern = re.compile(
        r'^(https?://)?'                   # optional http or https
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domain like oraclecloud.com
        r'(/[^\s]*)?$'                     # optional path
    )
    return bool(pattern.match(url))
