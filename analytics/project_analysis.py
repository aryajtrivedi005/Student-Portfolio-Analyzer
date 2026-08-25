import pandas as pd
from typing import Dict, Any, List
from analytics.scoring import clamp

def evaluate_single_project(project: Dict[str, Any], target_role: str) -> Dict[str, Any]:
    score = 0.0

    # 1. Complexity (Max 30 pts)
    comp = str(project.get('complexity', '')).capitalize()
    if comp == "Advanced":
        score += 30.0
    elif comp == "High":
        score += 25.0
    elif comp == "Medium":
        score += 20.0
    else:
        score += 10.0

    # 2. Deployment Status (Max 30 pts)
    status = str(project.get('deployment_status', '')).lower()
    if "deployed" in status and "not" not in status and "local" not in status:
        score += 30.0
        deployment_label = "Deployed"
    elif "in dev" in status:
        score += 15.0
        deployment_label = "In Development"
    else:
        score += 10.0
        deployment_label = "Local Only"

    # 3. Technology Stack Diversity (Max 20 pts)
    techs = [t.strip() for t in str(project.get('technologies', '')).split(',') if t.strip()]
    if len(techs) >= 4:
        score += 20.0
    elif len(techs) >= 2:
        score += 15.0
    else:
        score += 10.0

    # 4. GitHub / Documentation Evidence (Max 20 pts)
    url = str(project.get('github_url', ''))
    if url.startswith("http") and "github.com" in url:
        score += 20.0

    final_score = round(clamp(score), 1)

    # Strengths and Weaknesses
    strengths = []
    weaknesses = []

    if comp in ["Advanced", "High"]:
        strengths.append(f"High technical complexity ({comp})")
    if deployment_label == "Deployed":
        strengths.append("Live deployment evidence available")
    else:
        weaknesses.append("No cloud deployment evidence (Local project only)")

    if len(techs) >= 3:
        strengths.append(f"Diverse tech stack ({', '.join(techs[:3])})")

    if not url.startswith("http"):
        weaknesses.append("Missing public repository documentation link")

    return {
        "project_name": project.get('project_name'),
        "description": project.get('description'),
        "domain": project.get('domain'),
        "technologies": techs,
        "complexity": comp,
        "deployment_status": deployment_label,
        "score": final_score,
        "strengths": strengths,
        "weaknesses": weaknesses
    }

def analyze_projects(projects_df: pd.DataFrame, target_role: str) -> Dict[str, Any]:
    if projects_df.empty:
        return {
            "project_count": 0,
            "deployed_count": 0,
            "avg_project_score": 0.0,
            "projects_list": [],
            "overall_project_score": 0.0
        }

    evaluated_projects = []
    deployed_count = 0
    total_score = 0.0

    for _, row in projects_df.iterrows():
        eval_res = evaluate_single_project(dict(row), target_role)
        evaluated_projects.append(eval_res)
        total_score += eval_res['score']
        if eval_res['deployment_status'] == "Deployed":
            deployed_count += 1

    project_count = len(evaluated_projects)
    avg_score = round(total_score / project_count, 1)

    # Overall project portfolio score accounts for project count bonus
    count_bonus = min(20.0, project_count * 10.0)
    deployment_bonus = min(20.0, deployed_count * 10.0)

    overall_score = round(clamp((0.6 * avg_score) + (0.2 * count_bonus) + (0.2 * deployment_bonus)), 1)

    return {
        "project_count": project_count,
        "deployed_count": deployed_count,
        "avg_project_score": avg_score,
        "projects_list": evaluated_projects,
        "overall_project_score": overall_score
    }
