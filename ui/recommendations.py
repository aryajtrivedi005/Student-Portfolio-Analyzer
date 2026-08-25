import streamlit as st
import pandas as pd
from typing import Dict, Any
from ai.recommendation_engine import (
    generate_recommendations,
    generate_next_project_recommendation,
    generate_roadmap
)
from database.database import (
    save_recommendations,
    get_recommendation_progress,
    update_recommendation_status
)

def render_recommendations_page(readiness_data: Dict[str, Any], student_id: int):
    st.markdown("## 🤖 AI Recommendation Engine & Career Advisor")

    # 1. Top 5 Actionable Recommendations
    st.markdown("### 🎯 Top 5 Recommended Actions")
    recs = generate_recommendations(readiness_data)

    # Save to SQLite progress table if needed
    save_recommendations(student_id, recs)

    for idx, r in enumerate(recs, 1):
        p_class = "badge-high" if r['priority'] == 'HIGH' else ("badge-medium" if r['priority'] == 'MEDIUM' else "badge-low")
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom: 1rem; border-left: 4px solid {'#EF4444' if r['priority']=='HIGH' else '#F59E0B'};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#1E3A8A;">{idx}. {r['title']}</h4>
                <span class="badge {p_class}">{r['priority']} PRIORITY</span>
            </div>
            <p style="margin-top:0.5rem; margin-bottom:0; color:#374151;"><strong>Reason:</strong> {r['reason']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. ⭐ "WHAT SHOULD I BUILD NEXT?" FEATURE ⭐
    st.markdown("### ⭐ Recommended Next Project (\"What Should I Build Next?\")")
    next_proj = generate_next_project_recommendation(readiness_data)

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: white; padding: 1.5rem 2rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h3 style="color:#60A5FA; margin-top:0;">💡 {next_proj['title']}</h3>
        <p style="font-size:1.05rem; opacity:0.9;"><strong>Why this project?</strong> {next_proj['why']}</p>
        <p><strong>Technologies Covered:</strong> {', '.join(next_proj['techs'])}</p>
        <p><strong>Skills Improved:</strong> {', '.join(next_proj['skills_improved'])}</p>
        <p style="color:#34D399; font-weight:600;">Expected Outcome: {next_proj['expected_outcome']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. Personalized 30-Day Roadmap
    st.markdown("### 📅 Personalized 30-Day Action Roadmap")
    roadmap = generate_roadmap(readiness_data)

    r_cols = st.columns(4)
    for idx, item in enumerate(roadmap):
        with r_cols[idx % 4]:
            st.markdown(f"""
            <div class="metric-card" style="min-height:220px; border-top: 4px solid #2563EB;">
                <div style="font-size:0.8rem; font-weight:700; color:#2563EB;">{item['week']}</div>
                <div style="font-size:1rem; font-weight:700; color:#111827; margin-top:0.3rem;">{item['goal']}</div>
                <p style="font-size:0.85rem; color:#4B5563; margin-top:0.5rem;"><strong>Action:</strong> {item['action']}</p>
                <div style="font-size:0.8rem; color:#059669; font-weight:600; margin-top:0.5rem;">{item['outcome']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 4. Interactive Progress Tracking
    st.markdown("### 🔄 My Progress Tracker & Continuous Improvement")
    st.markdown("Track recommendation execution status. Update statuses and re-analyze your score!")

    progress_df = get_recommendation_progress(student_id)
    if not progress_df.empty:
        for _, row in progress_df.iterrows():
            col_t, col_s = st.columns([3, 1])
            with col_t:
                st.write(f"**{row['title']}** ({row['priority']} Priority)")
            with col_s:
                new_status = st.selectbox(
                    "Status",
                    ["Pending", "In Progress", "Completed"],
                    index=["Pending", "In Progress", "Completed"].index(row['status']),
                    key=f"status_select_{row['progress_id']}"
                )
                if new_status != row['status']:
                    update_recommendation_status(row['progress_id'], new_status)
                    st.toast(f"Updated '{row['title']}' to {new_status}!", icon="✅")

        if st.button("🔄 Re-analyze Portfolio", type="primary"):
            st.rerun()
