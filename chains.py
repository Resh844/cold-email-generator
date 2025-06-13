
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.5,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-70b-8192"
        )

    def write_mail(self, job, resume_text, project_summary):
        prompt = PromptTemplate.from_template("""
You are a final-year engineering student applying for the following job role.

### ROLE:
{job_description}

### RESUME DETAILS:
{resume_details}

### RELEVANT PROJECTS:
{link_list}

### TASK:
1. Generate a **professional cold email** with:
    - Clear greeting
    - Enthusiastic tone
    - Skill alignment with the role
    - Justify why you are a great fit
    - Include a "Relevant Projects" section
    - End with "Thanks and Regards"
    - Keep it within 200 words

2. Also generate a **relevant subject line**.

Output JSON only with:
```json
{{
  "subject": "...",
  "email": "..."
}}
""")

        chain = prompt | self.llm
        input_data = {
            "job_description": job["role"],
            "resume_details": resume_text,
            "link_list": project_summary,
        }

        result = chain.invoke(input_data)
        try:
            parsed = JsonOutputParser().parse(result.content)
            return parsed["email"], parsed["subject"]
        except Exception:
            return result.content, f"Application for {job['role']}"

    def write_cover_letter(self, job, resume_text, project_summary):
        prompt = PromptTemplate.from_template("""
    You are a final-year engineering student applying for the following job.

    ### ROLE:
    {job_description}

    ### RESUME DETAILS:
    {resume_details}

    ### PROJECTS:
    {link_list}

    ### TASK:
    Generate a well-structured **cover letter** with:
    - A formal header and greeting
    - Introduction with your enthusiasm for the role
    - Middle paragraph aligning your skills with the job
    - Relevant projects or experiences
    - Ending with thanks and readiness to discuss further
    - Max 300 words

    Output only the plain text of the cover letter.
    """)

        chain = prompt | self.llm
        input_data = {
            "job_description": job["role"],
            "resume_details": resume_text,
            "link_list": project_summary,
        }

        result = chain.invoke(input_data)
        return result.content.strip()
