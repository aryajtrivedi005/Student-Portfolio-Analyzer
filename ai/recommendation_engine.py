from typing import Dict, Any, List
from ai.ollama_client import ollama_client
from ai.prompts import (
    SYSTEM_PROMPT_ANALYST,
    RECOMMENDATIONS_PROMPT_TEMPLATE,
    NEXT_PROJECT_PROMPT_TEMPLATE,
    ROADMAP_PROMPT_TEMPLATE
)
from rag.vector_store import get_vector_store

def generate_deterministic_recommendations(readiness_data: Dict[str, Any]) -> List[Dict[str, str]]:
    recs = []
    target_role = readiness_data.get('target_role', 'Software Engineer')
    skill_analysis = readiness_data.get('skill_analysis', {})
    high_gaps = skill_analysis.get('high_priority_gaps', [])
    proj_analysis = readiness_data.get('project_analysis', {})
    acad_analysis = readiness_data.get('academic_analysis', {})
    breakdown = readiness_data.get('breakdown', {})

    # 1. Missing high priority skills
    if high_gaps:
        top_skill = high_gaps[0]['skill']
        recs.append({
            "title": f"Learn {top_skill} Fundamentals",
            "priority": "HIGH",
            "reason": f"{top_skill} is a critical missing skill gap for your target role as a {target_role}."
        })

    # 2. Deployment recommendation
    if proj_analysis.get('deployed_count', 0) == 0:
        recs.append({
            "title": "Deploy an Interactive Web / Model Service",
            "priority": "HIGH",
            "reason": "Your portfolio contains projects but lacks live cloud deployment evidence (e.g. Streamlit Cloud, AWS EC2, or Docker)."
        })

    # 3. MLOps / DevOps recommendation
    if "Machine Learning" in target_role or "Data" in target_role:
        if any(g['skill'] in ['Docker', 'Cloud', 'MLOps'] for g in high_gaps):
            recs.append({
                "title": "Build an MLOps Packaging Pipeline",
                "priority": "HIGH",
                "reason": "Top employers look for candidates who can package ML models into REST APIs (FastAPI) inside Docker containers."
            })
    elif "Software" in target_role or "Backend" in target_role:
        recs.append({
            "title": "Master Docker & Containerization",
            "priority": "HIGH",
            "reason": "Containerization using Docker is required to build production-grade microservices for backend engineering."
        })

    # 4. Academic / Attendance alert
    if acad_analysis.get('subjects_at_risk'):
        risk_subj = acad_analysis['subjects_at_risk'][0]['course']
        recs.append({
            "title": f"Improve Performance in {risk_subj}",
            "priority": "HIGH",
            "reason": f"Your current attendance/marks in {risk_subj} place you at risk. Attend upcoming review sessions."
        })
    else:
        recs.append({
            "title": "Enhance GitHub Documentation & READMEs",
            "priority": "MEDIUM",
            "reason": "Ensure all project repositories include visual architecture diagrams, installation guides, and API samples."
        })

    # 5. Internship / Experience gap
    if breakdown.get('Experience', 0) < 50:
        recs.append({
            "title": "Apply for Technical Internships or Open Source Contributions",
            "priority": "MEDIUM",
            "reason": "Adding practical industry experience or major GitHub pull requests will boost your career readiness score."
        })
    else:
        recs.append({
            "title": "Obtain Cloud Certification",
            "priority": "MEDIUM",
            "reason": f"Completing an industry-recognized cloud certificate will validate your skills for {target_role} positions."
        })

    return recs[:5]

def generate_recommendations(readiness_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate recommendations using Ollama if available, otherwise deterministic rules."""
    deterministic_recs = generate_deterministic_recommendations(readiness_data)

    if not ollama_client.is_available():
        return deterministic_recs

    # Try Ollama prompt
    target_role = readiness_data.get('target_role')
    name = readiness_data.get('student_name')
    high_gaps = [g['skill'] for g in readiness_data.get('skill_analysis', {}).get('high_priority_gaps', [])]
    projects_list = [p['project_name'] for p in readiness_data.get('project_analysis', {}).get('projects_list', [])]

    # Query RAG
    vector_store = get_vector_store()
    rag_docs = vector_store.search(f"{target_role} skill requirements deployment guidelines", top_k=2)
    rag_context = "\n---\n".join([d['content'] for d in rag_docs])

    prompt = RECOMMENDATIONS_PROMPT_TEMPLATE.format(
        name=name,
        target_role=target_role,
        cgpa=readiness_data.get('academic_analysis', {}).get('cgpa'),
        attendance_status=readiness_data.get('academic_analysis', {}).get('attendance_status'),
        career_score=readiness_data.get('career_readiness_score'),
        skill_gaps=", ".join(high_gaps) if high_gaps else "None",
        projects=", ".join(projects_list) if projects_list else "None",
        deployed_count=readiness_data.get('project_analysis', {}).get('deployed_count'),
        internships_count=len(readiness_data.get('strengths', [])),
        rag_context=rag_context
    )

    response = ollama_client.generate(prompt, system_prompt=SYSTEM_PROMPT_ANALYST)
    if response and len(response.strip()) > 50:
        # Parsed text response
        parsed = []
        lines = response.split('\n')
        curr = {}
        for line in lines:
            line_str = line.strip()
            if line_str and (line_str[0].isdigit() and ('.' in line_str[:3] or ')' in line_str[:3])):
                if curr and 'title' in curr:
                    parsed.append(curr)
                curr = {"title": line_str.split('.', 1)[-1].strip(), "priority": "HIGH", "reason": ""}
            elif curr and "priority:" in line_str.lower():
                curr['priority'] = line_str.split(':', 1)[-1].strip().upper()
            elif curr and "reason:" in line_str.lower():
                curr['reason'] = line_str.split(':', 1)[-1].strip()
            elif curr and line_str and not curr.get('reason'):
                curr['reason'] = line_str

        if curr and 'title' in curr:
            parsed.append(curr)

        if len(parsed) >= 3:
            return parsed[:5]

    return deterministic_recs

def generate_next_project_recommendation(readiness_data: Dict[str, Any]) -> Dict[str, Any]:
    target_role = readiness_data.get('target_role', 'Software Engineer')
    high_gaps = [g['skill'] for g in readiness_data.get('skill_analysis', {}).get('high_priority_gaps', [])]
    name = readiness_data.get('student_name', 'Student')

    # Default fallback project recommendation tailored to profile
    if "Machine Learning" in target_role or "Data" in target_role:
        fallback = {
            "title": "ML Model Deployment & Monitoring Microservice",
            "why": f"This project specifically targets your critical skill gaps in Docker, Cloud, and REST API deployment for {target_role}.",
            "techs": ["Python", "FastAPI", "Docker", "Scikit-Learn", "Streamlit Cloud"],
            "skills_improved": ["Docker", "MLOps", "REST APIs", "Cloud Deployment"],
            "expected_outcome": "A containerized ML prediction service deployed live on cloud with interactive Swagger docs."
        }
    elif "Cloud" in target_role or "DevOps" in target_role:
        fallback = {
            "title": "Automated Cloud Infrastructure & CI/CD Pipeline",
            "why": f"Builds hands-on evidence of Infrastructure as Code and cloud deployment required for {target_role}.",
            "techs": ["AWS", "Docker", "Kubernetes", "Terraform", "GitHub Actions"],
            "skills_improved": ["AWS", "Kubernetes", "DevOps", "CI/CD"],
            "expected_outcome": "Fully automated deployment pipeline deploying containerized web app to AWS."
        }
    else:
        fallback = {
            "title": "Scalable RESTful Microservices Architecture",
            "why": f"Demonstrates backend architecture, authentication, and database design expected for {target_role}.",
            "techs": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis"],
            "skills_improved": ["REST API", "Database", "Docker", "System Design"],
            "expected_outcome": "Production-grade backend service with Docker Compose orchestration."
        }

    if not ollama_client.is_available():
        return fallback

    student_skills = [s['name'] for s in readiness_data.get('skill_analysis', {}).get('student_skills', [])]
    existing_projs = [p['project_name'] for p in readiness_data.get('project_analysis', {}).get('projects_list', [])]

    prompt = NEXT_PROJECT_PROMPT_TEMPLATE.format(
        name=name,
        target_role=target_role,
        skills=", ".join(student_skills) if student_skills else "Python, SQL",
        skill_gaps=", ".join(high_gaps) if high_gaps else "Docker, Cloud",
        existing_projects=", ".join(existing_projs) if existing_projs else "Basic local projects"
    )

    response = ollama_client.generate(prompt, system_prompt=SYSTEM_PROMPT_ANALYST)
    if response and "PROJECT TITLE:" in response:
        try:
            res_dict = {}
            for line in response.split('\n'):
                if "PROJECT TITLE:" in line:
                    res_dict['title'] = line.split("PROJECT TITLE:", 1)[1].strip()
                elif "WHY THIS PROJECT:" in line:
                    res_dict['why'] = line.split("WHY THIS PROJECT:", 1)[1].strip()
                elif "TECHNOLOGIES COVERED:" in line:
                    res_dict['techs'] = [t.strip() for t in line.split("TECHNOLOGIES COVERED:", 1)[1].split(',')]
                elif "SKILLS IMPROVED:" in line:
                    res_dict['skills_improved'] = [s.strip() for s in line.split("SKILLS IMPROVED:", 1)[1].split(',')]
                elif "EXPECTED OUTCOME:" in line:
                    res_dict['expected_outcome'] = line.split("EXPECTED OUTCOME:", 1)[1].strip()
            if res_dict.get('title'):
                return {
                    "title": res_dict.get('title', fallback['title']),
                    "why": res_dict.get('why', fallback['why']),
                    "techs": res_dict.get('techs', fallback['techs']),
                    "skills_improved": res_dict.get('skills_improved', fallback['skills_improved']),
                    "expected_outcome": res_dict.get('expected_outcome', fallback['expected_outcome'])
                }
        except Exception:
            pass

    return fallback

def generate_roadmap(readiness_data: Dict[str, Any]) -> List[Dict[str, str]]:
    target_role = readiness_data.get('target_role', 'Software Engineer')
    high_gaps = [g['skill'] for g in readiness_data.get('skill_analysis', {}).get('high_priority_gaps', [])]
    g1 = high_gaps[0] if high_gaps else "Docker"
    g2 = high_gaps[1] if len(high_gaps) > 1 else "Cloud Deployment"

    fallback = [
        {
            "week": "Week 1",
            "goal": f"Learn Core {g1} Fundamentals",
            "action": f"Complete hands-on tutorials on {g1} container creation and CLI commands.",
            "outcome": f"Understand core {g1} concepts and write configuration files.",
            "priority": "HIGH"
        },
        {
            "week": "Week 2",
            "goal": "Build REST API Service",
            "action": "Develop a FastAPI/Flask endpoint wrapping your existing project logic.",
            "outcome": "Expose working HTTP endpoints with input validation.",
            "priority": "HIGH"
        },
        {
            "week": "Week 3",
            "goal": f"Containerize & Deploy ({g2})",
            "action": f"Package application into Docker container and deploy to {g2} or Streamlit Cloud.",
            "outcome": "Obtain live public web URL for portfolio evidence.",
            "priority": "HIGH"
        },
        {
            "week": "Week 4",
            "goal": "GitHub Documentation & Portfolio Sync",
            "action": "Create visual architecture diagram, write clean README.md, and update resume.",
            "outcome": "Complete verified evidence portfolio entry.",
            "priority": "MEDIUM"
        }
    ]

    return fallback
