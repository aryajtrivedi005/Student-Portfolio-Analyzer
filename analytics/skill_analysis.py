import pandas as pd
from typing import Dict, Any, List
from analytics.scoring import clamp

def analyze_skills(skills_df: pd.DataFrame, target_role: str, career_reqs_df: pd.DataFrame) -> Dict[str, Any]:
    student_skills_map = {}
    if not skills_df.empty:
        for _, row in skills_df.iterrows():
            student_skills_map[row['skill_name'].strip().lower()] = {
                "name": row['skill_name'].strip(),
                "category": row['category'],
                "proficiency": float(row['proficiency'])
            }

    # Categorize skills into Strong (>=80), Moderate (60-79), Needs Improvement (<60)
    categorized = {"Strong": [], "Moderate": [], "Needs Improvement": []}
    for sk, info in student_skills_map.items():
        prof = info['proficiency']
        if prof >= 80.0:
            categorized["Strong"].append(info)
        elif prof >= 60.0:
            categorized["Moderate"].append(info)
        else:
            categorized["Needs Improvement"].append(info)

    # Skill Gap Matrix vs Target Role Requirements
    skill_gaps = []
    total_req_weight = 0.0
    weighted_achievement = 0.0

    if not career_reqs_df.empty:
        for _, req in career_reqs_df.iterrows():
            req_skill = req['skill'].strip()
            req_skill_lower = req_skill.lower()
            req_prof = float(req['required_proficiency'])
            importance = req['importance']

            weight = 3.0 if importance == "High" else (2.0 if importance == "Medium" else 1.0)
            total_req_weight += weight * req_prof

            student_prof = student_skills_map.get(req_skill_lower, {}).get("proficiency", 0.0)
            gap = round(student_prof - req_prof, 1)

            weighted_achievement += weight * min(student_prof, req_prof)

            priority = "HIGH" if (gap < -15 and importance in ["High", "Medium"]) or student_prof == 0 else (
                "MEDIUM" if gap < 0 else "LOW"
            )

            skill_gaps.append({
                "skill": req_skill,
                "required": req_prof,
                "student": student_prof,
                "gap": gap,
                "importance": importance,
                "priority": priority
            })

    # High priority gaps (skills needed urgently)
    high_priority_gaps = [g for g in skill_gaps if g['priority'] == 'HIGH']
    # Sort by gap magnitude ascending (most negative first)
    high_priority_gaps.sort(key=lambda x: x['gap'])

    # Technical skill score (0-100)
    if total_req_weight > 0:
        tech_score = round(clamp((weighted_achievement / total_req_weight) * 100.0), 1)
    elif not skills_df.empty:
        tech_score = round(skills_df['proficiency'].mean(), 1)
    else:
        tech_score = 0.0

    return {
        "student_skills": list(student_skills_map.values()),
        "categorized": categorized,
        "skill_gaps": skill_gaps,
        "high_priority_gaps": high_priority_gaps,
        "technical_skill_score": tech_score,
        "total_skills_count": len(student_skills_map)
    }
