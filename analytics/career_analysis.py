import pandas as pd
from typing import Dict, Any, List
from analytics.academic_analysis import analyze_academics
from analytics.skill_analysis import analyze_skills
from analytics.project_analysis import analyze_projects
from analytics.scoring import clamp

def calculate_career_readiness(
    student: Dict[str, Any],
    academic_records_df: pd.DataFrame,
    skills_df: pd.DataFrame,
    projects_df: pd.DataFrame,
    certs_df: pd.DataFrame,
    internships_df: pd.DataFrame,
    activities_df: pd.DataFrame,
    career_reqs_df: pd.DataFrame
) -> Dict[str, Any]:

    target_role = student.get('target_role', 'Software Engineer')

    # 1. Academic Performance (20%)
    acad_res = analyze_academics(academic_records_df, float(student.get('cgpa', 0.0)))
    acad_score = acad_res['academic_score']

    # 2. Technical Skills (25%)
    skill_res = analyze_skills(skills_df, target_role, career_reqs_df)
    skill_score = skill_res['technical_skill_score']

    # 3. Projects (20%)
    proj_res = analyze_projects(projects_df, target_role)
    proj_score = proj_res['overall_project_score']

    # 4. Internship / Experience (15%)
    intern_count = len(internships_df)
    if intern_count >= 3:
        intern_score = 100.0
    elif intern_count == 2:
        intern_score = 85.0
    elif intern_count == 1:
        intern_score = 70.0
    else:
        intern_score = 30.0

    # 5. Certifications (10%)
    cert_count = len(certs_df)
    if cert_count >= 3:
        cert_score = 100.0
    elif cert_count == 2:
        cert_score = 80.0
    elif cert_count == 1:
        cert_score = 60.0
    else:
        cert_score = 20.0

    # 6. Extracurricular Activities (10%)
    act_count = len(activities_df)
    if act_count >= 3:
        act_score = 100.0
    elif act_count == 2:
        act_score = 80.0
    elif act_count == 1:
        act_score = 65.0
    else:
        act_score = 30.0

    # Calculate Weighted Career Readiness Score
    weighted_score = (
        (acad_score * 0.20) +
        (skill_score * 0.25) +
        (proj_score * 0.20) +
        (intern_score * 0.15) +
        (cert_score * 0.10) +
        (act_score * 0.10)
    )

    career_readiness_score = round(clamp(weighted_score), 1)

    # Breakdown mapping
    breakdown = {
        "Academics": acad_score,
        "Technical Skills": skill_score,
        "Projects": proj_score,
        "Experience": intern_score,
        "Certifications": cert_score,
        "Activities": act_score
    }

    # Strengths and Weaknesses identification
    strengths = []
    weaknesses = []
    alerts = []

    if acad_score >= 80:
        strengths.append(f"Strong Academic Performance (CGPA: {student.get('cgpa')})")
    elif acad_score < 70:
        weaknesses.append(f"Academics below standard benchmark (CGPA: {student.get('cgpa')})")

    if acad_res['subjects_at_risk']:
        for s in acad_res['subjects_at_risk']:
            if s['att_risk']:
                alerts.append(f"⚠ Attendance risk in {s['course']} ({s['attendance']}%)")
            if s['mark_risk']:
                alerts.append(f"⚠ Low marks in {s['course']} ({s['marks']}%)")

    if skill_score >= 80:
        strengths.append("High technical skill alignment for target role")
    elif skill_score < 65:
        weaknesses.append(f"Technical skill gap for target role '{target_role}'")

    if skill_res['high_priority_gaps']:
        top_missing = [g['skill'] for g in skill_res['high_priority_gaps'][:3]]
        weaknesses.append(f"Critical missing skills for {target_role}: {', '.join(top_missing)}")
        alerts.append(f"⚠ High priority skill gaps detected: {', '.join(top_missing)}")

    if proj_score >= 80:
        strengths.append(f"Solid project portfolio ({proj_res['project_count']} projects)")
    elif proj_res['deployed_count'] == 0:
        weaknesses.append("Portfolio lacks live cloud-deployed project evidence")
        alerts.append("⚠ Portfolio lacks live deployment evidence")

    if intern_count > 0:
        strengths.append(f"Practical internship experience ({intern_count} completed)")
    else:
        weaknesses.append("No industry internship or professional experience")
        alerts.append("⚠ No internship experience recorded")

    if cert_count > 0:
        strengths.append(f"Industry certifications verified ({cert_count} certificates)")

    return {
        "student_id": student.get('student_id'),
        "student_name": student.get('name'),
        "target_role": target_role,
        "career_readiness_score": career_readiness_score,
        "breakdown": breakdown,
        "academic_analysis": acad_res,
        "skill_analysis": skill_res,
        "project_analysis": proj_res,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "alerts": alerts
    }
