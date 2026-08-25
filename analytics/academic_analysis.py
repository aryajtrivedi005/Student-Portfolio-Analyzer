import pandas as pd
from typing import Dict, Any
from analytics.scoring import normalize_cgpa, clamp

def analyze_academics(records_df: pd.DataFrame, cgpa: float) -> Dict[str, Any]:
    if records_df.empty:
        return {
            "cgpa": cgpa,
            "avg_marks": 0.0,
            "best_subject": "N/A",
            "weakest_subject": "N/A",
            "avg_attendance": 0.0,
            "subjects_at_risk": [],
            "academic_score": normalize_cgpa(cgpa),
            "grade_distribution": {},
            "attendance_status": "Unknown"
        }

    avg_marks = round(records_df['marks'].mean(), 2)
    avg_att = round(records_df['attendance'].mean(), 2)

    best_row = records_df.loc[records_df['marks'].idxmax()]
    weak_row = records_df.loc[records_df['marks'].idxmin()]

    best_subject = f"{best_row['course']} ({best_row['marks']}%)"
    weakest_subject = f"{weak_row['course']} ({weak_row['marks']}%)"

    # Identify subjects at risk: attendance < 75% or marks < 65
    subjects_at_risk = []
    for _, row in records_df.iterrows():
        is_att_risk = row['attendance'] < 75.0
        is_mark_risk = row['marks'] < 65.0
        if is_att_risk or is_mark_risk:
            subjects_at_risk.append({
                "course": row['course'],
                "marks": row['marks'],
                "attendance": row['attendance'],
                "att_risk": is_att_risk,
                "mark_risk": is_mark_risk,
                "recommendation": (
                    "Attend upcoming classes immediately to maintain 75% eligibility."
                    if is_att_risk else "Complete practice problems and review core concepts."
                )
            })

    # Grade distribution
    grade_counts = records_df['grade'].value_counts().to_dict()

    # Academic score calculation: 60% CGPA + 40% Average Marks
    cgpa_norm = normalize_cgpa(cgpa)
    academic_score = round(clamp((0.6 * cgpa_norm) + (0.4 * avg_marks)), 1)

    # Attendance classification
    if avg_att >= 85.0:
        att_status = "Good"
    elif avg_att >= 75.0:
        att_status = "Moderate"
    else:
        att_status = "At Risk"

    return {
        "cgpa": cgpa,
        "avg_marks": avg_marks,
        "best_subject": best_subject,
        "weakest_subject": weakest_subject,
        "avg_attendance": avg_att,
        "subjects_at_risk": subjects_at_risk,
        "academic_score": academic_score,
        "grade_distribution": grade_counts,
        "attendance_status": att_status
    }
