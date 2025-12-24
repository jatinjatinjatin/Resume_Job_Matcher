import streamlit as st
import requests
import fitz
import re
from collections import Counter
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="📄Resume & Job Matcher", page_icon="📄", layout="centered")
st.title("📄Resume & Job Matcher")
st.caption("ATS-grade resume analysis.")

st.sidebar.header("ℹ️ Setup Instructions")
st.sidebar.markdown("Install Ollama → https://ollama.ai and run `ollama run llama3`")

MODEL_NAME = st.sidebar.text_input("Ollama Model Name", value="llama3")

def extract_pdf_text(file):
    text = []
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            t = page.get_text("text")
            if t:
                text.append(t)
    return "\n".join(text)

def extract_keywords(text):
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    stop = {
        "and","the","with","for","this","that","from","you","are","was",
        "were","have","has","will","your","job","role","skills","experience"
    }
    return [w for w in words if w not in stop]

def call_ollama(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
        timeout=180
    )
    return r.json().get("response", "")

def generate_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []
    for line in text.split("\n"):
        if line.strip():
            content.append(Paragraph(line, styles["Normal"]))
            content.append(Spacer(1, 10))
    doc.build(content)
    buffer.seek(0)
    return buffer

st.subheader("📤 Upload Files")
resume_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf","txt"])
job_files = st.file_uploader("Upload Job Descriptions (PDF/TXT)", type=["pdf","txt"], accept_multiple_files=True)

if st.button("🔍 Analyze Resume", use_container_width=True):
    if not resume_file or not job_files:
        st.warning("Please upload resume and job descriptions.")
        st.stop()

    resume_text = extract_pdf_text(resume_file) if resume_file.type=="application/pdf" else resume_file.read().decode("utf-8", errors="ignore")
    resume_keywords = extract_keywords(resume_text)
    report = []

    for idx, job_file in enumerate(job_files, start=1):
        job_text = extract_pdf_text(job_file) if job_file.type=="application/pdf" else job_file.read().decode("utf-8", errors="ignore")
        job_keywords = extract_keywords(job_text)
        matched = set(resume_keywords).intersection(set(job_keywords))
        ats_score = int((len(matched) / max(len(set(job_keywords)), 1)) * 100)

        prompt = f"""
You are an ATS resume evaluation AI.

Return:
## Fit Score (0–100%)
## Strengths
## Skill Gaps
## Resume Improvements
## Recruiter Verdict

RESUME:
{resume_text[:12000]}

JOB DESCRIPTION:
{job_text[:12000]}
"""

        with st.spinner(f"Analyzing Job #{idx}..."):
            ai_result = call_ollama(prompt)

        st.subheader(f"Job Match #{idx}")
        st.metric("ATS Score", f"{ats_score}%")
        st.markdown(ai_result)

        report.append(f"JOB #{idx}\nATS SCORE: {ats_score}%\n{ai_result}\n")

    st.session_state["final_report"] = "\n".join(report)

if "final_report" in st.session_state:
    pdf = generate_pdf(st.session_state["final_report"])
    st.download_button("📤 Download PDF Report", pdf, "resume_job_match_report.pdf", "application/pdf")
