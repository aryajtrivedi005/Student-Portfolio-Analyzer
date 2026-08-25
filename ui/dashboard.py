import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

def render_dashboard(readiness_data: Dict[str, Any]):
    st.markdown("## 🏠 Executive Overview Dashboard")
    st.markdown(f"**Target Role:** `{readiness_data.get('target_role')}` | **Student:** `{readiness_data.get('student_name')}`")

    # 1. Top KPI Row
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    acad_analysis = readiness_data.get('academic_analysis', {})
    skill_analysis = readiness_data.get('skill_analysis', {})
    proj_analysis = readiness_data.get('project_analysis', {})

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">CGPA</div>
            <div class="value">{acad_analysis.get('cgpa', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        att = acad_analysis.get('avg_attendance', 0.0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Attendance</div>
            <div class="value" style="color: {'#EF4444' if att < 75 else '#10B981'};">{att}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Skills</div>
            <div class="value">{skill_analysis.get('total_skills_count', 0)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Projects</div>
            <div class="value">{proj_analysis.get('project_count', 0)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Deployed</div>
            <div class="value" style="color: {'#EF4444' if proj_analysis.get('deployed_count', 0) == 0 else '#10B981'};">
                {proj_analysis.get('deployed_count', 0)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        exp_score = readiness_data.get('breakdown', {}).get('Experience', 0)
        has_exp = "Yes" if exp_score > 50 else "No"
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Internship</div>
            <div class="value">{has_exp}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. Main Career Readiness Gauge & Breakdown
    left_col, right_col = st.columns([1.2, 1.8])

    with left_col:
        score = readiness_data.get('career_readiness_score', 0.0)
        st.markdown(f"""
        <div class="gauge-container">
            <div class="gauge-label">Career Readiness Index</div>
            <div class="gauge-score">{score}</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #E2E8F0; margin-top: 0.3rem;">out of 100</div>
        </div>
        """, unsafe_allow_html=True)

        # Plotly Radial Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                'bar': {'color': "#3B82F6"},
                'steps': [
                    {'range': [0, 50], 'color': "#FEE2E2"},
                    {'range': [50, 75], 'color': "#FEF3C7"},
                    {'range': [75, 100], 'color': "#D1FAE5"}
                ],
            }
        ))
        fig_gauge.update_layout(height=180, margin=dict(l=20, r=20, t=10, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with right_col:
        st.markdown("### 📊 Readiness Dimension Breakdown")
        breakdown = readiness_data.get('breakdown', {})
        for dim, val in breakdown.items():
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**{dim}**")
                st.progress(min(1.0, max(0.0, val / 100.0)))
            with col_b:
                st.markdown(f"<span style='font-size:1.1rem; font-weight:700; color:#1E3A8A;'>{val}%</span>", unsafe_allow_html=True)

    st.markdown("---")

    # 3. Dynamic Alerts, Strengths & Weaknesses
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("### 🟢 Top Strengths")
        strengths = readiness_data.get('strengths', [])
        if strengths:
            for s in strengths:
                st.markdown(f"""
                <div class="alert-success">
                    ✓ <strong>{s}</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No notable strengths recorded yet.")

    with c_right:
        st.markdown("### 🔴 Critical Weaknesses & Gaps")
        weaknesses = readiness_data.get('weaknesses', [])
        if weaknesses:
            for w in weaknesses:
                st.markdown(f"""
                <div class="alert-danger">
                    ⚠ <strong>{w}</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No critical weaknesses detected!")

    alerts = readiness_data.get('alerts', [])
    if alerts:
        st.markdown("### ⚠ Immediate Attention Required")
        for alt in alerts:
            st.markdown(f"""
            <div class="alert-warning">
                {alt}
            </div>
            """, unsafe_allow_html=True)
