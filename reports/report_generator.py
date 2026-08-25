import io
import pandas as pd
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_csv_export(readiness_data: Dict[str, Any]) -> str:
    rows = []
    rows.append(["Metric", "Value"])
    rows.append(["Student Name", readiness_data.get("student_name")])
    rows.append(["Target Role", readiness_data.get("target_role")])
    rows.append(["Career Readiness Score", f"{readiness_data.get('career_readiness_score')}/100"])

    breakdown = readiness_data.get("breakdown", {})
    for k, v in breakdown.items():
        rows.append([f"Score - {k}", f"{v}/100"])

    acad = readiness_data.get("academic_analysis", {})
    rows.append(["CGPA", acad.get("cgpa")])
    rows.append(["Average Marks", f"{acad.get('avg_marks')}%"])
    rows.append(["Attendance Average", f"{acad.get('avg_attendance')}%"])
    rows.append(["Attendance Status", acad.get("attendance_status")])

    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df.to_csv(index=False)

def generate_pdf_report(readiness_data: Dict[str, Any]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#1E3A8A"), spaceAfter=12)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#1F2937"), spaceBefore=10, spaceAfter=6)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor("#374151"), leading=14)

    elements = []

    # Title
    elements.append(Paragraph("Student360 AI - Executive Career Readiness Report", title_style))
    elements.append(Spacer(1, 10))

    # Profile Table
    name = readiness_data.get("student_name", "N/A")
    target_role = readiness_data.get("target_role", "N/A")
    score = readiness_data.get("career_readiness_score", 0.0)

    profile_data = [
        ["Student Name:", name, "Target Career:", target_role],
        ["Career Readiness Score:", f"{score} / 100", "Report Date:", "August 2026"]
    ]
    t_profile = Table(profile_data, colWidths=[130, 150, 110, 150])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F3F4F6")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#1F2937")),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB"))
    ]))
    elements.append(t_profile)
    elements.append(Spacer(1, 15))

    # Readiness Score Breakdown Table
    elements.append(Paragraph("Score Breakdown by Dimension", heading_style))
    breakdown = readiness_data.get("breakdown", {})
    bd_data = [["Dimension", "Weight", "Score / 100"]]
    weights = {"Academics": "20%", "Technical Skills": "25%", "Projects": "20%", "Experience": "15%", "Certifications": "10%", "Activities": "10%"}
    for dim, sc in breakdown.items():
        bd_data.append([dim, weights.get(dim, "-"), f"{sc}"])

    t_bd = Table(bd_data, colWidths=[200, 150, 190])
    t_bd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2563EB")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB"))
    ]))
    elements.append(t_bd)
    elements.append(Spacer(1, 15))

    # Key Strengths & Weaknesses
    elements.append(Paragraph("Strengths & Priority Weaknesses", heading_style))
    strengths = readiness_data.get("strengths", [])
    weaknesses = readiness_data.get("weaknesses", [])

    st_text = "<b>Strengths:</b><br/>" + "<br/>".join([f"• {s}" for s in strengths]) if strengths else "None"
    wk_text = "<b>Weaknesses & Gaps:</b><br/>" + "<br/>".join([f"• {w}" for w in weaknesses]) if weaknesses else "None"

    sw_data = [[Paragraph(st_text, body_style), Paragraph(wk_text, body_style)]]
    t_sw = Table(sw_data, colWidths=[270, 270])
    t_sw.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#ECFDF5")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#FEF2F2")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB"))
    ]))
    elements.append(t_sw)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
