import streamlit as st
from typing import Dict, Any
from reports.report_generator import generate_pdf_report, generate_csv_export

def render_reports_page(readiness_data: Dict[str, Any]):
    st.markdown("## 📊 Reports & Executive Export")
    st.markdown(f"Generate professional student reports and CSV analytics for **{readiness_data.get('student_name')}**.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="metric-card" style="border-top: 4px solid #2563EB;">
            <h3>📄 Executive PDF Student Report</h3>
            <p>Comprehensive PDF summary including Career Readiness score, grade breakdown, skill gap matrix, and top recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)

        pdf_bytes = generate_pdf_report(readiness_data)
        st.download_button(
            label="📥 Download Executive PDF Report",
            data=pdf_bytes,
            file_name=f"{readiness_data.get('student_name').replace(' ', '_')}_Career_Readiness_Report.pdf",
            mime="application/pdf",
            type="primary"
        )

    with col2:
        st.markdown("""
        <div class="metric-card" style="border-top: 4px solid #10B981;">
            <h3>📈 CSV Analytics Export</h3>
            <p>Export complete analytical facts and readiness breakdown into tabular CSV format for further analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)

        csv_data = generate_csv_export(readiness_data)
        st.download_button(
            label="📥 Export CSV Analytics Data",
            data=csv_data,
            file_name=f"{readiness_data.get('student_name').replace(' ', '_')}_analytics.csv",
            mime="text/csv"
        )

    st.markdown("---")
    st.markdown("### 👁 Executive Report Preview")
    st.json({
        "Student Name": readiness_data.get("student_name"),
        "Target Role": readiness_data.get("target_role"),
        "Career Readiness Score": f"{readiness_data.get('career_readiness_score')} / 100",
        "Dimension Breakdown": readiness_data.get("breakdown"),
        "Top Strengths": readiness_data.get("strengths"),
        "Critical Weaknesses": readiness_data.get("weaknesses"),
        "Immediate Alerts": readiness_data.get("alerts")
    })
