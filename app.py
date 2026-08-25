import streamlit as st
import pandas as pd
import os

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Student360 AI — Student Portfolio & Career Readiness Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database & Seed Data
from database.database import (
    init_db,
    get_all_students,
    get_student_by_id,
    get_academic_records,
    get_skills,
    get_projects,
    get_certificates,
    get_internships,
    get_activities,
    get_career_requirements,
    get_all_career_roles
)
from analytics.career_analysis import calculate_career_readiness
from ui.styles import apply_custom_styles
from ui.dashboard import render_dashboard
from ui.academic import render_academic_analytics
from ui.skills import render_skills_portfolio
from ui.career import render_career_readiness
from ui.recommendations import render_recommendations_page
from ui.assistant import render_ai_assistant
from ui.portfolio_upload import render_portfolio_upload
from ui.reports import render_reports_page
from ui.university import render_university_view
from ai.ollama_client import ollama_client

# Initialize SQLite database
init_db()

# Apply CSS styling
apply_custom_styles()

# Main Header Banner
st.markdown("""
<div class="app-header">
    <h1>🎓 Student360 AI</h1>
    <p>AI-Powered Student Portfolio & Career Readiness Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Setup
st.sidebar.markdown("## ⚙️ Control Panel")

# Mode Switch: Student View vs University View
app_mode = st.sidebar.radio("View Mode", ["Student View", "University View"], index=0)

if app_mode == "University View":
    render_university_view()
else:
    # 1-CLICK HACKATHON DEMO MODE BUTTON
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚀 Hackathon Demo Mode")
    if st.sidebar.button("✨ Launch Demo (Rahul Patel)", type="primary", use_container_width=True):
        st.session_state['selected_student_id'] = 1
        st.session_state['selected_target_role'] = "Machine Learning Engineer"
        st.session_state['nav_page'] = "🏠 Dashboard"
        st.rerun()

    st.sidebar.markdown("---")

    # Fetch All Students & Roles
    students_df = get_all_students()
    all_roles = get_all_career_roles()

    if students_df.empty:
        st.error("No student profiles found. Please initialize the database.")
        st.stop()

    # Default selection handling
    student_names = students_df['name'].tolist()
    default_student_idx = 0
    if 'selected_student_id' in st.session_state:
        for idx, row in students_df.iterrows():
            if row['student_id'] == st.session_state['selected_student_id']:
                default_student_idx = idx
                break

    selected_student_name = st.sidebar.selectbox("Select Student", student_names, index=default_student_idx)
    selected_student_row = students_df[students_df['name'] == selected_student_name].iloc[0]
    student_id = int(selected_student_row['student_id'])

    # Target Career Selector
    default_target_role = selected_student_row['target_role']
    if 'selected_target_role' in st.session_state and selected_student_name == "Rahul Patel":
        default_target_role = st.session_state['selected_target_role']

    default_role_idx = all_roles.index(default_target_role) if default_target_role in all_roles else 0
    target_role = st.sidebar.selectbox("Target Career Role", all_roles, index=default_role_idx)

    # Navigation Menu
    st.sidebar.markdown("---")
    nav_options = [
        "🏠 Dashboard",
        "📚 Academic Analytics",
        "💻 Skills & Portfolio",
        "🎯 Career Readiness",
        "🤖 AI Recommendations",
        "💬 AI Student Assistant",
        "📄 Portfolio Upload",
        "📊 Reports",
        "ℹ️ About"
    ]
    default_nav_idx = 0
    if 'nav_page' in st.session_state and st.session_state['nav_page'] in nav_options:
        default_nav_idx = nav_options.index(st.session_state['nav_page'])

    page = st.sidebar.radio("Navigation", nav_options, index=default_nav_idx)

    # Privacy & Ollama Status Indicator in Sidebar
    st.sidebar.markdown("---")
    is_ollama_online = ollama_client.is_available()
    ollama_model = ollama_client.select_best_model() if is_ollama_online else None

    if is_ollama_online:
        st.sidebar.success(f"🟢 Local AI (Ollama): Active\nModel: `{ollama_model}`")
    else:
        st.sidebar.warning("🟡 Local AI (Ollama): Offline\nRunning in Deterministic Mode")

    st.sidebar.caption("🔒 Privacy First: All student portfolio data processed locally.")

    # FETCH LIVE DATA & CALCULATE CAREER READINESS FOR SELECTED STUDENT
    student_dict = get_student_by_id(student_id)
    student_dict['target_role'] = target_role

    academic_records_df = get_academic_records(student_id)
    skills_df = get_skills(student_id)
    projects_df = get_projects(student_id)
    certs_df = get_certificates(student_id)
    internships_df = get_internships(student_id)
    activities_df = get_activities(student_id)
    career_reqs_df = get_career_requirements(target_role)

    # DYNAMIC SCORING ENGINE EXECUTION
    readiness_data = calculate_career_readiness(
        student_dict,
        academic_records_df,
        skills_df,
        projects_df,
        certs_df,
        internships_df,
        activities_df,
        career_reqs_df
    )

    # ROUTE PAGES
    if page == "🏠 Dashboard":
        render_dashboard(readiness_data)

    elif page == "📚 Academic Analytics":
        render_academic_analytics(academic_records_df, readiness_data['academic_analysis'])

    elif page == "💻 Skills & Portfolio":
        render_skills_portfolio(
            skills_df,
            projects_df,
            certs_df,
            internships_df,
            readiness_data['skill_analysis'],
            readiness_data['project_analysis'],
            target_role
        )

    elif page == "🎯 Career Readiness":
        render_career_readiness(readiness_data, certs_df, internships_df, activities_df)

    elif page == "🤖 AI Recommendations":
        render_recommendations_page(readiness_data, student_id)

    elif page == "💬 AI Student Assistant":
        render_ai_assistant(readiness_data, student_dict)

    elif page == "📄 Portfolio Upload":
        render_portfolio_upload(student_id, selected_student_name)

    elif page == "📊 Reports":
        render_reports_page(readiness_data)

    elif page == "ℹ️ About":
        st.markdown("## ℹ️ About Student360 AI")
        st.markdown("""
        **Student360 AI** is an intelligent digital portfolio & career readiness analytics platform built for university students and administrators.

        ### Key Technical Innovations:
        1. **Deterministic + Generative AI Hybrid**: Hard facts (CGPA, marks, attendance, skill proficiency) are calculated via SQLite & Pandas algorithms, while LLMs (Ollama) provide contextual explanations, roadmap synthesis, and advice.
        2. **Skill Gap Matrix & Evidence Verification**: Cross-references self-reported skills against concrete evidence in projects, certifications, and internships.
        3. **RAG Knowledge Base**: Uses local vector search to retrieve career role benchmarks and placement guidelines.
        4. **Local-First & Resilient**: Works offline without cloud API keys, with full rule-based fallback if local LLM servers are offline.

        Built for **TCS Technology Day at Nirma University**.
        """)
