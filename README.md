# 🎓 Student360 AI — Student Portfolio & Career Readiness Analyzer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🚀 **Live Production Application:** [https://student360.streamlit.app](https://student360.streamlit.app)

**Student360 AI** is an intelligent full-stack digital portfolio and career readiness analytics platform built with Python, Streamlit, SQLite, Pandas, and RAG vector search.

It provides a 360-degree evaluation of a student's academic standing, skill proficiencies, project quality, attendance risks, and career readiness against target industry roles (*Software Engineer, Machine Learning Engineer, Data Scientist, Cloud Engineer, etc.*).

---

## 🌟 Key Features

* **Dynamic 6-Part Weighted Scoring Engine:** Calculates Career Readiness (0-100) across Academics (20%), Technical Skills (25%), Projects (20%), Experience (15%), Certifications (10%), and Extracurriculars (10%).
* **⭐ Skill Gap Matrix:** Compares student skills against target career role benchmarks to compute precise percentage gaps (*e.g., Docker -25%, Cloud -35%, MLOps -40%*).
* **⭐ Evidence-Based Skill Verification:** Cross-references self-reported skills against tangible proof in GitHub repositories, certificates, and internships to compute **Evidence Confidence %**.
* **Document OCR & Skill Extraction:** Scans PDF resumes and certificate images (PNG/JPG) using OpenCV and PyTesseract OCR to sync skills directly into SQLite.
* **Resilient Hybrid AI System:** Uses local Ollama LLMs for explanations and natural language advice, with automatic fallback to deterministic rules when running on cloud servers.
* **Executive PDF & CSV Reports:** Generates downloadable ReportLab executive summaries and raw CSV analytics.
* **University Administration Dashboard:** Aggregated anonymized statistics and AI campus policy recommendations for university deans and placement departments.

---

## 🏗 System Architecture

```text
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│     SQLite Database       │ ───> │  Pandas Analytics Engine  │ ───> │ Deterministic Scoring Math│
│  (8 Relational Tables)    │      │  (Data Transformation)    │      │   (Readiness 0-100)       │
└───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘
                                                                                    │
┌───────────────────────────┐      ┌───────────────────────────┐                    ▼
│  Streamlit SaaS Dashboard │ <─── │   RAG Vector Store & AI   │ <──────────────────┘
│   (Multi-Page App UI)     │      │   (Placement Context)     │
└───────────────────────────┘      └───────────────────────────┘
```

---

## 🛠 Technology Stack

* **Frontend & Web UI:** Streamlit, Custom SaaS HTML/CSS, Plotly Interactive Charts
* **Analytics Engine:** Python 3.10+, Pandas, NumPy, SQLite3
* **AI & RAG System:** Ollama Local API (`llama3`), TF-IDF Vector Search Knowledge Base
* **OCR & Document Processing:** PyTesseract, OpenCV, PyPDF
* **Reporting:** ReportLab (Executive PDF generation) & CSV export

---

## 💻 Local Installation & Setup

```bash
# 1. Clone Repository
git clone https://github.com/YOUR_USERNAME/student360-ai.git
cd student360-ai

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Launch Application
python -m streamlit run app.py
```

The application will be accessible at `http://localhost:8501`.

---

## 📝 Resume Bullet Points (Copy & Paste)

```text
Student360 AI — Full-Stack Student Analytics & Career Readiness Platform
Live App: https://student360.streamlit.app | GitHub: github.com/YOUR_USERNAME/student360-ai
• Developed a full-stack student portfolio evaluation platform using Python, Streamlit, SQLite, and Pandas.
• Engineered a 6-part weighted scoring algorithm calculating dynamic readiness indices (0-100) and skill gap matrices against target career benchmarks.
• Built evidence verification routines cross-referencing self-claimed skills against project tech stacks, certificate records, and OCR extracted documents.
• Integrated RAG vector search for placement guidelines and ReportLab for automated executive PDF report generation.
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
