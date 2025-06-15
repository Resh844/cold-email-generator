import streamlit as st
from utils import extract_resume_text, extract_skills_projects, extract_keywords_from_job_description, match_resume_keywords, is_valid_url
from chains import Chain
from langchain_community.document_loaders import WebBaseLoader
import time
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

# 🔧 Helper: JS-based clipboard button
def clipboard_button(text, key):
    btn_id = f"copy-btn-{key}"
    components.html(f"""
        <textarea id="text-{key}" style="position:absolute; left:-1000px; top:-1000px;">{text}</textarea>
        <button id="{btn_id}" style="padding:5px 10px;border-radius:8px;border:none;color:black;font-weight:bold;cursor:pointer;">
            ⧉ Copy to Clipboard
        </button>
        <script>
            const btn = document.getElementById("{btn_id}");
            btn.onclick = function() {{
                const txt = document.getElementById("text-{key}");
                txt.select();
                document.execCommand("copy");
                btn.innerText = "☑️ Copied!";
                setTimeout(() => {{
                    btn.innerText = "⧉ Copy to Clipboard";
                }}, 2000);
            }};
        </script>
    """, height=50)

st.set_page_config(page_title="Cold Email & Cover Letter Generator", layout="centered")
st.title("✉️ Cold Email & Cover Letter Generator")
st.markdown("Built with **LLaMA 3**, LangChain, and Groq API")

# ✅ Custom CSS
st.markdown("""
    <style>
    .stButton > button {
        background-color: #007BcF;
        color: black;
        padding: 8px 20px;
        border: none;
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    textarea[data-baseweb="textinput"] {
        height: 30px !important;
        resize: none !important;
        overflow: hidden !important;
        font-size: 14px !important;
        padding-top: 10px !important;
    }
    @media only screen and (max-width: 600px) {
        button, input, select, textarea {
            width: 100% !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

chain = Chain()

with st.sidebar:
    st.header("Upload & Personalize")

    st.markdown('<label style="font-weight:600;">📄 Upload Resume (PDF/DOCX) <span style="color:red;">*</span></label>', unsafe_allow_html=True)
    resume_file = st.file_uploader("", type=["pdf", "docx"], key="resume")

    st.markdown('<label style="font-weight:600;">📎 LinkedIn Profile URL (optional)</label>', unsafe_allow_html=True)
    linkedin_url = st.text_input(label="LinkedIn URL",placeholder="https://www.linkedin.com/in/yourname", key="linkedin_url",label_visibility="collapsed")

    st.markdown('<label style="font-weight:600;">💼 Target Job Roles <span style="color:red;">*</span></label>', unsafe_allow_html=True)
    common_roles = [
        "Frontend Developer", "Backend Developer", "Full Stack Developer",
        "Machine Learning Intern", "Data Analyst", "DevOps Engineer",
        "Software Engineer", "AI Research Intern", "Product Manager"
    ]
    selected_roles = st.multiselect("Select from common roles", options=common_roles, help="You can select multiple roles", key="selected_roles")
    custom_role = st.text_input("Other (if not listed above)", placeholder="e.g., Blockchain Developer", key="custom_role")
    roles_input = selected_roles + ([custom_role] if custom_role else [])

    st.markdown('<label style="font-weight:600;">Job Posting URL <span style="color:red;">*</span></label>', unsafe_allow_html=True)
    job_url = st.text_input("🔗Job Posting URL", placeholder="Job Posting URL Link",key="job_url")

    st.markdown('<p style="color:gray;font-size:14px;"><span style="color:red;">*</span> Required fields</p>', unsafe_allow_html=True)

# ✅ Generate Button Outside Sidebar
generate_clicked = st.button("Generate Cold Email + Cover Letter")

if generate_clicked:
    if not resume_file or not roles_input or not job_url:
        st.error("Please fill in all required fields (resume, roles, and job URL).")
        st.stop()

    if not is_valid_url(job_url):
        st.error("Please enter a valid job URL.")
        st.stop()

    messages = [
        "🔍 Loading the job description...",
        "👁️‍🗨️ Loading the job description...",
        "📄 Parsing your resume...",
        "💭 Matching skills and keywords...",
        "👜 Finding excellent skills to add...",
        "✒️ Generating personalized content...",
    ]
    placeholder = st.empty()
    for msg in messages:
        placeholder.info(msg)
        time.sleep(1.2)
    placeholder.success("☑️ Done!")

    resume_text = extract_resume_text(resume_file)

    if linkedin_url:
        try:
            response = requests.get(linkedin_url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.content, "html.parser")
            summary_section = soup.find("section", {"class": "summary"})
            linkedin_summary = summary_section.get_text(strip=True) if summary_section else ""
            resume_text += f"\n\nLinkedIn Summary:\n{linkedin_summary}"
        except:
            pass

    try:
        loader = WebBaseLoader([job_url])
        job_text = loader.load().pop().page_content
    except Exception as e:
        st.error(f"Could not load job description: {e}")
        st.stop()

    roles = [r.strip() for r in roles_input if r.strip()]
    st.session_state.results = []

    for i, role in enumerate(roles, start=1):
        job = {"role": role}
        project_summary = extract_skills_projects(resume_text).get("projects", "")
        email_text, subject = chain.write_mail(job, resume_text, project_summary)
        cover_letter = chain.write_cover_letter(job, resume_text, project_summary)
        email_text += "\n\n📎 *Don't forget to attach your resume before sending!*"
        keywords = extract_keywords_from_job_description(role)
        matched, missing = match_resume_keywords(resume_text, keywords)

        st.session_state.results.append({
            "i": i,
            "role": role,
            "email_text": email_text,
            "cover_letter": cover_letter,
            "subject": subject,
            "matched": matched,
            "missing": missing
        })

if "results" in st.session_state and st.session_state.results:
    for res in st.session_state.results:
        st.markdown(f"## Results for: `{res['role']}`")

        tab1, tab2, tab3 = st.tabs(["📧 Cold Email", "📄 Cover Letter", "📘 Keyword Match"])

        with tab1:
            st.markdown(f"### ✉️ Subject Line: `{res['subject']}`")
            st.text_area("📧 Cold Email Preview", res["email_text"], height=250, key=f"email_text_area_{res['i']}")
            st.download_button("📥 Download Cold Email", res["email_text"], file_name=f"cold_email_{res['role']}.txt", key=f"dl_email_{res['i']}")
            clipboard_button(res["email_text"], key=f"email_{res['i']}")

        with tab2:
            st.text_area("📄 Cover Letter Preview", res["cover_letter"], height=300, key=f"cover_letter_text_area_{res['i']}")
            st.download_button("💾 Download Cover Letter", res["cover_letter"], file_name=f"cover_letter_{res['role']}.txt", key=f"dl_cover_{res['i']}")
            clipboard_button(res["cover_letter"], key=f"cover_{res['i']}")

        with tab3:
            st.markdown("📘 **Keyword Match Summary**:")
            st.write(f"Matched: {', '.join(res['matched']) if res['matched'] else 'None'}")
            st.write(f"Missing: {', '.join(res['missing']) if res['missing'] else 'None'}")
else:
    st.info("🪧 Upload your resume, add job roles, and paste job URL to begin.")
