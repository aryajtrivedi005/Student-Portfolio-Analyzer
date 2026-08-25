# Student360 AI — AI-Powered Student Portfolio & Career Readiness Analyzer

> **TCS Technology Day at Nirma University Hackathon Submission**  
> **Use Case 45: Student Portfolio Analyzer**

---

## 📌 Product Overview

**Student360 AI** is a complete, intelligent student analytics and career readiness web platform built using Streamlit, Python, SQLite, Pandas, and Ollama Local AI.

It provides a 360-degree evaluation of a student's:
* Academic performance & attendance risk (<75%)
* Technical skill proficiencies & categorization
* Skill gap analysis vs target career role benchmarks
* Portfolio project complexity & cloud deployment status
* Evidence-based skill confidence verification
* Industry internship & certification records
* Personalized AI recommendations, "What Should I Build Next?" advisor, and 30-Day Roadmaps
* Context-aware conversational AI student assistant (RAG)
* Certificate OCR & Resume parsing into SQLite
* PDF & CSV report exports
* Aggregate University Administrator view

---

## 🏗 System Architecture

```text
[ SQLite Database ] ──> [ Pandas DataFrames ] ──> [ Deterministic Analytics & Scoring Engine ]
                                                                │
                                                                ▼
[ User Interface ]  <── [ Local Ollama AI / RAG ] <── [ Career Readiness Score (0-100) ]
(Streamlit Dashboard)
```

---

## 🛠 Technology Stack

* **Frontend & Dashboard:** Streamlit, Custom SaaS HTML/CSS, Plotly Charts
* **Backend Data Analytics:** Python 3.10+, Pandas, NumPy, SQLite3
* **AI & LLM Integration:** Local Ollama (supports Llama 3.x, Mistral, Gemma, Phi-3) with automatic model auto-detection & deterministic fallback engine
* **RAG & Knowledge Retrieval:** TF-IDF Cosine Vector Retrieval Knowledge Base
* **OCR & Document Processing:** PyTesseract, OpenCV, PyPDF
* **Reporting:** ReportLab (Executive PDF generation) & CSV export

---

## 📁 Project Structure

```text
c:/Users/lll/OneDrive/Desktop/TCS Hackathon/
├── app.py                      # Main Streamlit application launcher & routing
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation & setup instructions
├── .gitignore                  # Git ignore rules
│
├── database/
│   ├── database.py             # SQLite connection & query helpers
│   ├── schema.sql              # Database DDL schema definition
│   └── seed_data.py            # Generates 15 realistic student profiles (Rahul Patel for Demo)
│
├── ai/
│   ├── ollama_client.py        # Ollama local AI API client & model selection
│   ├── prompts.py              # Prompt engineering templates
│   └── recommendation_engine.py# AI & deterministic recommendation advisors
│
├── analytics/
│   ├── academic_analysis.py    # Academic overview, marks & attendance risk (<75%)
│   ├── skill_analysis.py       # Skill gap matrix vs target career requirements
│   ├── project_analysis.py     # Deterministic project quality & deployment evaluator
│   ├── career_analysis.py      # Dynamic 6-part weighted Career Readiness score (0-100)
│   ├── scoring.py              # Score normalization math utilities
│   └── evidence_verifier.py    # Cross-verifies claimed skills against tangible portfolio evidence
│
├── rag/
│   ├── vector_store.py         # Vector search retriever
│   └── knowledge_base.py       # Domain guidelines knowledge base
│
├── document_processing/
│   ├── document_parser.py      # PDF text extractor
│   ├── ocr.py                  # OpenCV / PyTesseract OCR scanner
│   └── portfolio_extractor.py  # Structured skill/cert parser for SQLite
│
├── reports/
│   └── report_generator.py     # ReportLab PDF & CSV export engine
│
└── ui/
    ├── styles.py               # SaaS CSS styles
    ├── dashboard.py            # Main executive dashboard
    ├── academic.py             # Academic analytics & attendance warnings
    ├── skills.py               # Skill Gap Matrix & Evidence Verification
    ├── career.py               # Career readiness breakdown
    ├── recommendations.py      # Top 5 Recommendations, "What Should I Build Next?", 30-Day Roadmap
    ├── assistant.py            # Context-aware AI Chat assistant
    ├── portfolio_upload.py     # OCR & Resume upload view
    ├── reports.py              # Executive reports view
    └── university.py           # Admin aggregate view
```

---

## 🚀 Setup & Installation Instructions

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Install Dependencies
Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### 3. (Optional) Ollama Setup for Local AI
Student360 AI works **100% offline out-of-the-box** using deterministic fallback rules.  
To enable rich local LLM AI generation:

1. Install Ollama from [ollama.ai](https://ollama.ai/).
2. Start the Ollama server:
   ```bash
   ollama serve
   ```
3. Pull a model (e.g., Llama 3):
   ```bash
   ollama pull llama3
   ```
The application will automatically detect running Ollama models!

---

## 💻 Running the Application

Launch the Streamlit web application:

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

---

## 🎬 Hackathon Demo Flow

1. Click **`✨ Launch Demo (Rahul Patel)`** in the left sidebar.
2. Observe **Rahul Patel** targeting **Machine Learning Engineer** (CGPA 8.4).
3. **Career Readiness Score:** View the dynamically calculated score of **`68 / 100`**.
4. **Academic Analytics:** Notice the attendance alert in *Computer Networks (69% attendance, At Risk)*.
5. **⭐ Skill Gap Matrix:** Navigate to `💻 Skills & Portfolio` -> `⭐ Skill Gap Matrix`. Highlight the critical missing gaps for ML Engineer:
   - Docker (-25%)
   - Cloud (-35%)
   - MLOps (-40%)
6. **⭐ Evidence Verification:** Notice how Python is verified (95%), while Docker and AWS show low evidence confidence.
7. **AI Recommendations:** Navigate to `🤖 AI Recommendations`. Observe top priority actions (Learn Docker, Deploy ML project, Build MLOps pipeline).
8. **⭐ "What Should I Build Next?":** View the recommended project: **ML Model Deployment & Monitoring Microservice**.
9. **Personalized 30-Day Roadmap:** View the 4-week structured improvement plan.
10. **💬 AI Student Assistant:** Ask: *"Why is my career readiness score 68?"* or *"What skills am I missing?"*. Notice the context-aware answer grounded in Rahul's database facts.
11. **📄 Portfolio Upload:** Test scanning a certificate image and click `➕ Add Certificate to Portfolio`.
12. **📊 Reports:** Download the executive PDF and CSV report.
13. **🏛 University View:** Toggle to `University View` in sidebar to inspect anonymized cohort stats and AI campus recommendations.
