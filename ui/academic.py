import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, Any

def render_academic_analytics(academic_df: pd.DataFrame, acad_analysis: Dict[str, Any]):
    st.markdown("## 📚 Academic Analytics & Attendance Monitor")

    if academic_df.empty:
        st.warning("No academic records found for this student.")
        return

    # Top KPI Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("CGPA", acad_analysis.get('cgpa'))
    with m2:
        st.metric("Average Marks", f"{acad_analysis.get('avg_marks')}%")
    with m3:
        att = acad_analysis.get('avg_attendance')
        st.metric("Avg Attendance", f"{att}%", delta="At Risk" if att < 75 else "Good", delta_color="inverse" if att < 75 else "normal")
    with m4:
        risk_count = len(acad_analysis.get('subjects_at_risk', []))
        st.metric("Subjects at Risk", risk_count, delta="Action Needed" if risk_count > 0 else "Clear", delta_color="inverse" if risk_count > 0 else "normal")

    st.markdown("---")

    # Interactive Charts
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📈 Marks by Subject")
        fig_marks = px.bar(
            academic_df,
            x='course',
            y='marks',
            color='marks',
            color_continuous_scale='Blues',
            text='marks',
            labels={'course': 'Course', 'marks': 'Marks (%)'}
        )
        fig_marks.update_layout(xaxis_tickangle=-30, height=350, showlegend=False)
        st.plotly_chart(fig_marks, use_container_width=True)

    with col_right:
        st.markdown("### ⏱ Attendance by Subject")
        fig_att = px.bar(
            academic_df,
            x='course',
            y='attendance',
            color='attendance',
            color_continuous_scale='RdYlGn',
            range_color=[50, 100],
            text='attendance',
            labels={'course': 'Course', 'attendance': 'Attendance (%)'}
        )
        fig_att.add_hline(y=75.0, line_dash="dash", line_color="red", annotation_text="75% Risk Threshold")
        fig_att.update_layout(xaxis_tickangle=-30, height=350, showlegend=False)
        st.plotly_chart(fig_att, use_container_width=True)

    st.markdown("---")

    # Detailed Table & Attendance Warning Cards
    st.markdown("### 📋 Subject Performance Breakdown")
    st.dataframe(
        academic_df[['course', 'marks', 'grade', 'attendance', 'semester']],
        use_container_width=True,
        hide_index=True
    )

    # Attendance & Marks Risk Warnings
    at_risk = acad_analysis.get('subjects_at_risk', [])
    if at_risk:
        st.markdown("### ⚠ Academic Attention Needed")
        for item in at_risk:
            st.markdown(f"""
            <div class="alert-danger">
                <h4>⚠ {item['course']}</h4>
                <p><strong>Marks:</strong> {item['marks']}% | <strong>Attendance:</strong> {item['attendance']}%</p>
                <p><strong>Recommendation:</strong> {item['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("🎉 All courses satisfy academic and attendance requirements (>75% attendance).")
