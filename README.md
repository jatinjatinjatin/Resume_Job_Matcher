# Resume_Job_Matcher
An ATS-grade resume analysis tool built with Streamlit and Ollama that compares resumes against job descriptions. It provides keyword-based ATS scoring, skill gap analysis, and AI-powered feedback to help candidates improve resume relevance for specific roles.


🚀 Features

📄 Resume Parsing
Supports PDF and TXT resumes using PyMuPDF.

🧾 Multiple Job Description Comparison
Analyze a single resume against multiple job descriptions in one run.

📈 ATS Keyword Match Score
Calculates a percentage score based on keyword overlap between the resume and job description, simulating real ATS behavior.

🧠 AI-Powered Analysis (Local LLM)
Uses Ollama (llama3 or compatible models) to provide:

Fit score (0–100%)

Key strengths

Skill gaps

Resume improvement suggestions

Recruiter-style verdict

🔐 Privacy-First & Offline
All analysis runs locally — no resume data is sent to external cloud services.

⚡ Interactive UI
Built with Streamlit for fast, clean, and user-friendly interaction.

🛠️ Tech Stack

Python

Streamlit – UI framework

Ollama – Local LLM runtime

Llama 3 – Language model

PyMuPDF (fitz) – PDF parsing

Requests – API communication

ReportLab – PDF report generation (optional feature)


1️⃣ Install dependencies
pip install streamlit requests pymupdf reportlab


2️⃣ Install & run Ollama

Download from: https://ollama.ai

Run a model locally:

ollama run llama3


▶️ Usage
streamlit run app.py

📊 Output Includes

ATS keyword match percentage

Resume strengths aligned to the job

Missing or weak skills

Actionable resume improvement suggestions

Recruiter-style evaluation summary

🎯 Use Cases

Job seekers optimizing resumes for ATS systems

Students preparing for placements

Career coaches and mentors

Resume screening simulations

AI/ML portfolio project
