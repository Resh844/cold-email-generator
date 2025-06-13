# # app/utils.py
# import pdfplumber
# from docx import Document
# from io import BytesIO
# import re

# def extract_resume_text(uploaded_file):
#     file_bytes = uploaded_file.read()
#     if uploaded_file.type == "application/pdf":
#         with pdfplumber.open(BytesIO(file_bytes)) as pdf:
#             text = "\n".join(page.extract_text() or "" for page in pdf.pages)
#     elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#         doc = Document(BytesIO(file_bytes))
#         text = "\n".join(p.text for p in doc.paragraphs)
#     else:
#         text = ""
#     return clean_text(text)

# def clean_text(text):
#     return re.sub(r"\s+", " ", text).strip()

# def extract_keywords_from_job_description(description):
#     # Very basic keyword extraction from role text
#     return [kw.strip().lower() for kw in re.split(r"[,\n]", description) if len(kw.strip()) > 2]

# def match_resume_keywords(resume_text, keywords):
#     resume_lower = resume_text.lower()
#     matched = [kw for kw in keywords if kw in resume_lower]
#     missing = [kw for kw in keywords if kw not in resume_lower]
#     return matched, missing

# def extract_skills_projects(text):
#     skills = re.findall(r"(Skills|Technical Skills|Proficiencies)\s*[:\-]?\s*(.*)", text, re.IGNORECASE)
#     projects = re.findall(r"(Projects|Relevant Projects)\s*[:\-]?\s*(.*)", text, re.IGNORECASE)
#     return {
#         "skills": skills[0][1] if skills else "",
#         "projects": projects[0][1] if projects else ""
#     }




# utils.py
# import pdfplumber
# import docx2txt
# from io import BytesIO
# import re

# def extract_text_from_pdf(pdf_bytes):
#     text = ""
#     try:
#         with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
#             for page in pdf.pages:
#                 page_text = page.extract_text()
#                 if page_text:
#                     text += page_text + "\n"
#     except Exception as e:
#         return f"ERROR: Failed to read PDF file - {str(e)}"
#     return text.strip()

# def extract_text_from_docx(docx_bytes):
#     try:
#         with BytesIO(docx_bytes) as docx_file:
#             return docx2txt.process(docx_file).strip()
#     except Exception as e:
#         return f"ERROR: Failed to read DOCX file - {str(e)}"

# def extract_resume_text(uploaded_file):
#     if uploaded_file.type == "application/pdf":
#         return extract_text_from_pdf(uploaded_file.read())
#     elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#         return extract_text_from_docx(uploaded_file.read())
#     else:
#         return "ERROR: Unsupported file format. Please upload PDF or DOCX."

# def extract_skills_projects(resume_text):
#     projects = []
#     lines = resume_text.splitlines()
#     project_keywords = ["project", "developed", "built", "created", "implemented"]
#     for line in lines:
#         if any(keyword in line.lower() for keyword in project_keywords):
#             projects.append(line.strip())
#     return {"projects": "\n".join(projects)}

# def extract_keywords_from_job_description(description):
#     words = re.findall(r'\b\w+\b', description.lower())
#     common_words = {"and", "the", "with", "you", "for", "are", "our", "your", "this", "that"}
#     keywords = list(set(word for word in words if word not in common_words and len(word) > 3))
#     return keywords

# def match_resume_keywords(resume_text, keywords):
#     matched = []
#     missing = []
#     lower_resume = resume_text.lower()
#     for keyword in keywords:
#         if keyword in lower_resume:
#             matched.append(keyword)
#         else:
#             missing.append(keyword)
#     return matched, missing













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
