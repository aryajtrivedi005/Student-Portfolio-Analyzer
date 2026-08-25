import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, Any, List
from analytics.evidence_verifier import verify_skills_evidence

def render_skills_portfolio(skills_df: pd.DataFrame, projects_df: pd.DataFrame, certs_df: pd.DataFrame, internships_df: pd.DataFrame, skill_analysis: Dict[str, Any], proj_analysis: Dict[str, Any], target_role: str):
    st.markdown("## 💻 Skills, Projects & Evidence Verification")

    tab1, tab2, tab3, tab4 = st.tabs(["⭐ Skill Gap Matrix", "🎯 Evidence Verification", "🛠 Technical Skills", "🚀 Projects Evaluator"])

    # TAB 1: SKILL GAP MATRIX ⭐
    with tab1:
        st.markdown(f"### 🎯 Skill Gap Analysis vs Target Role: `{target_role}`")
        gaps = skill_analysis.get('skill_gaps', [])
        if gaps:
            gaps_df = pd.DataFrame(gaps)

            # High Priority Gaps Callout
            high_gaps = [g for g in gaps if g['priority'] == 'HIGH']
            if high_gaps:
                st.markdown("#### 🚨 HIGH PRIORITY SKILL GAPS DETECTED")
                cols = st.columns(min(4, len(high_gaps)))
                for idx, g in enumerate(high_gaps[:4]):
                    with cols[idx % 4]:
                        st.markdown(f"""
                        <div class="alert-danger" style="text-align: center;">
                            <div style="font-size:1.2rem; font-weight:700;">{g['skill']}</div>
                            <div style="font-size:0.9rem;">Target: {g['required']}% | Student: {g['student']}%</div>
                            <div style="font-size:1.1rem; font-weight:800; color:#EF4444; margin-top:0.3rem;">Gap: {g['gap']}%</div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("#### 📊 Comparative Requirement Matrix")

            fig_gap = px.bar(
                gaps_df,
                x='skill',
                y=['required', 'student'],
                barmode='group',
                title=f"Required vs Student Proficiency for {target_role}",
                labels={'value': 'Proficiency (%)', 'skill': 'Skill Name', 'variable': 'Category'},
                color_discrete_map={'required': '#94A3B8', 'student': '#2563EB'}
            )
            fig_gap.update_layout(height=400)
            st.plotly_chart(fig_gap, use_container_width=True)

            # Full Gap Table
            st.dataframe(
                gaps_df[['skill', 'importance', 'required', 'student', 'gap', 'priority']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info(f"No specific career benchmark requirements configured for '{target_role}'.")

    # TAB 2: EVIDENCE VERIFICATION ⭐
    with tab2:
        st.markdown("### 🔍 Evidence-Based Skill Verification")
        st.markdown("Cross-references self-claimed student skills against concrete proof in GitHub projects, certificates, and internships.")

        evidence_list = verify_skills_evidence(skills_df, projects_df, certs_df, internships_df)
        if evidence_list:
            ev_df = pd.DataFrame(evidence_list)
            st.dataframe(
                ev_df[['status_icon', 'skill_name', 'claimed_proficiency', 'confidence_pct', 'status', 'evidence_sources']],
                use_container_width=True,
                hide_index=True
            )

            st.markdown("#### 🏆 Verification Breakdown")
            for ev in evidence_list:
                c1, c2, c3 = st.columns([2, 4, 2])
                with c1:
                    st.write(f"**{ev['skill_name']}**")
                with c2:
                    st.progress(ev['confidence_pct'] / 100.0)
                with c3:
                    st.markdown(f"**{ev['status_icon']} {ev['confidence_pct']}%** ({ev['status']})")

    # TAB 3: TECHNICAL SKILLS
    with tab3:
        st.markdown("### 🛠 Categorized Skill Proficiencies")
        categorized = skill_analysis.get('categorized', {})

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("#### 🟢 Strong (>= 80%)")
            for sk in categorized.get('Strong', []):
                st.write(f"**{sk['name']}** ({sk['category']})")
                st.progress(sk['proficiency'] / 100.0)

        with c2:
            st.markdown("#### 🟡 Moderate (60-79%)")
            for sk in categorized.get('Moderate', []):
                st.write(f"**{sk['name']}** ({sk['category']})")
                st.progress(sk['proficiency'] / 100.0)

        with c3:
            st.markdown("#### 🔴 Needs Improvement (< 60%)")
            for sk in categorized.get('Needs Improvement', []):
                st.write(f"**{sk['name']}** ({sk['category']})")
                st.progress(sk['proficiency'] / 100.0)

    # TAB 4: PROJECTS EVALUATOR
    with tab4:
        st.markdown("### 🚀 Project Quality & Deployment Analysis")
        projs = proj_analysis.get('projects_list', [])
        if projs:
            for p in projs:
                with st.expander(f"📌 {p['project_name']} — Score: {p['score']}/100 ({p['deployment_status']})"):
                    st.write(f"**Description:** {p['description']}")
                    st.write(f"**Domain:** {p['domain']} | **Complexity:** {p['complexity']}")
                    st.write(f"**Technologies:** {', '.join(p['technologies'])}")

                    col_st, col_wk = st.columns(2)
                    with col_st:
                        st.markdown("**Strengths:**")
                        for s in p['strengths']:
                            st.write(f"✓ {s}")
                    with col_wk:
                        st.markdown("**Weaknesses / Improvement Areas:**")
                        for w in p['weaknesses']:
                            st.write(f"⚠ {w}")
        else:
            st.info("No projects found in student database.")
