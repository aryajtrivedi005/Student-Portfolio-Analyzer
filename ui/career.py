import streamlit as st
import pandas as pd
from typing import Dict, Any

def render_career_readiness(readiness_data: Dict[str, Any], certs_df: pd.DataFrame, internships_df: pd.DataFrame, activities_df: pd.DataFrame):
    st.markdown(f"## 🎯 Career Readiness Matrix: `{readiness_data.get('target_role')}`")

    # Overall Summary Banner
    score = readiness_data.get('career_readiness_score', 0.0)
    st.markdown(f"""
    <div class="alert-success" style="background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%); color: white;">
        <h3 style="margin:0; color:white;">Overall Readiness Score: {score} / 100</h3>
        <p style="margin-top:0.3rem; opacity:0.9;">Evaluated against industry standards for <strong>{readiness_data.get('target_role')}</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    # 1. Internships & Experience
    with c1:
        st.markdown("### 💼 Industry Internships")
        if not internships_df.empty:
            for _, row in internships_df.iterrows():
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-weight:700; font-size:1.1rem;">{row['company']}</div>
                    <div style="color:#2563EB; font-weight:600;">{row['role']}</div>
                    <div style="font-size:0.85rem; color:#6B7280;">Domain: {row['domain']}</div>
                    <div style="font-size:0.85rem; color:#6B7280;">Duration: {row['duration']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br/>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-danger">
                ⚠ <strong>No Internship Experience Recorded</strong><br/>
                Completing an industry internship increases career readiness by 15%.
            </div>
            """, unsafe_allow_html=True)

    # 2. Verified Certificates
    with c2:
        st.markdown("### 📜 Certifications")
        if not certs_df.empty:
            for _, row in certs_df.iterrows():
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-weight:700; font-size:1rem;">{row['certificate_name']}</div>
                    <div style="color:#059669; font-weight:600;">{row['issuer']}</div>
                    <div style="font-size:0.85rem; color:#6B7280;">Category: {row['category']} | Date: {row['date']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br/>", unsafe_allow_html=True)
        else:
            st.info("No certifications recorded.")

    # 3. Extracurricular Activities
    with c3:
        st.markdown("### 🏆 Activities & Leadership")
        if not activities_df.empty:
            for _, row in activities_df.iterrows():
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-weight:700; font-size:1rem;">{row['activity_name']}</div>
                    <div style="color:#D97706; font-weight:600;">Role: {row['participation_level']}</div>
                    <div style="font-size:0.85rem; color:#6B7280;">Category: {row['category']} ({row['date']})</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br/>", unsafe_allow_html=True)
        else:
            st.info("No extracurricular activities recorded.")
