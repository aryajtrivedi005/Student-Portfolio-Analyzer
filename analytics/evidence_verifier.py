import pandas as pd
from typing import Dict, Any, List

def verify_skills_evidence(skills_df: pd.DataFrame, projects_df: pd.DataFrame, certs_df: pd.DataFrame, internships_df: pd.DataFrame) -> List[Dict[str, Any]]:
    if skills_df.empty:
        return []

    # Extract text corpuses for matching
    project_techs = []
    if not projects_df.empty:
        for techs in projects_df['technologies'].dropna():
            project_techs.extend([t.strip().lower() for t in str(techs).split(',')])
        for desc in projects_df['description'].dropna():
            project_techs.append(str(desc).lower())

    cert_corpuses = []
    if not certs_df.empty:
        for _, row in certs_df.iterrows():
            cert_corpuses.append(f"{row['certificate_name']} {row['category']} {row['issuer']}".lower())

    internship_corpuses = []
    if not internships_df.empty:
        for _, row in internships_df.iterrows():
            internship_corpuses.append(f"{row['role']} {row['domain']} {row['company']}".lower())

    verified_results = []

    for _, row in skills_df.iterrows():
        skill_name = str(row['skill_name']).strip()
        skill_lower = skill_name.lower()
        prof = float(row['proficiency'])

        # Evidence checks
        has_proj_evidence = any(skill_lower in pt for pt in project_techs)
        has_cert_evidence = any(skill_lower in cc for cc in cert_corpuses)
        has_intern_evidence = any(skill_lower in ic for ic in internship_corpuses)

        confidence = 15.0 # Base self-claimed score
        evidence_sources = []

        if has_proj_evidence:
            confidence += 45.0
            evidence_sources.append("Project Tech Stack")
        if has_cert_evidence:
            confidence += 25.0
            evidence_sources.append("Verified Certificate")
        if has_intern_evidence:
            confidence += 25.0
            evidence_sources.append("Work Internship")

        confidence = min(100.0, confidence)

        if confidence >= 75.0:
            status = "Verified"
            status_icon = "✓"
        elif confidence >= 45.0:
            status = "Moderate Evidence"
            status_icon = "⚠"
        else:
            status = "Unverified Claim"
            status_icon = "✗"

        verified_results.append({
            "skill_name": skill_name,
            "category": row['category'],
            "claimed_proficiency": prof,
            "has_projects": has_proj_evidence,
            "has_certs": has_cert_evidence,
            "has_internship": has_intern_evidence,
            "confidence_pct": round(confidence, 1),
            "status": status,
            "status_icon": status_icon,
            "evidence_sources": ", ".join(evidence_sources) if evidence_sources else "None (Self-reported)"
        })

    return verified_results
