# 📧 Cold Email & Cover Letter Generator

An AI-powered web app that helps students generate **cold emails** and **cover letters** for multiple job roles using their **resume**, **LinkedIn profile**, and **job description links**.

Built with:

- 🧠 LLaMA 3 (via Groq API)
- 🔗 LangChain
- ⚡ Streamlit
- 📄 PDF/DOCX Parsing
- 💡 Keyword Matching

---

## 🚀 Features

- Upload resume (PDF/DOCX)
- Parse and summarize LinkedIn profile (optional)
- Match skills with job descriptions
- Generate **cold emails** and **cover letters** using LLMs
- Download or copy results instantly
- Keyword match summary for ATS-style feedback

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq LLM API (LLaMA 3.1)
- BeautifulSoup
- Requests
- pdfplumber / python-docx

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cold-email-generator.git
cd cold-email-generator
```

### 2.Create a Virtual Environment

```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Set API Key

You can set your API Key using.env file
Store the API Key in the .env file

---

## ▶️ Run the App

```bash
streamlit run main.py
```

Then open your browser and go to:  
http://localhost:8501

---

## 📁 Project Structure

```
cold-email-generator/
├── main.py              # Streamlit interface
├── chains.py            # LangChain chains
├── utils.py             # Resume + keyword parsing
├── portfolio.py         # Section-wise resume parser
├── requirements.txt     # Required libraries
└── README.md            # You're reading this :)
```

---

## 👩‍💻 Author

**Reshma Hegde**  
Student, B.E. in Information Science, Global Academy of Technology, Bangalore  
Passionate about AI/ML, GenAI, and real-world impactful software solutions 💡

---

## 💬 Feedback & Contributions

If you found this useful, please ⭐ the repo!

Contributions, bug reports, and pull requests are welcome 🙌
