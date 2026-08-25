import os
import sqlite3
import pandas as pd
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "student360.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database and seed data if DB does not exist or tables are empty."""
    db_exists = os.path.exists(DB_PATH)
    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()

    # Check if students exist
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        from database.seed_data import seed_database
        seed_database()

def get_all_students() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM students ORDER BY name ASC", conn)
    conn.close()
    return df

def get_student_by_id(student_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_academic_records(student_id: int) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM academic_records WHERE student_id = ?", conn, params=(student_id,))
    conn.close()
    return df

def get_skills(student_id: int) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM skills WHERE student_id = ?", conn, params=(student_id,))
    conn.close()
    return df

def get_projects(student_id: int) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM projects WHERE student_id = ?", conn, params=(student_id,))
    conn.close()
    return df

def get_certificates(student_id: int) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM certificates WHERE student_id = ?", conn, params=(student_id,))
    conn.close()
    return df

def get_internships(student_id: int) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM internships WHERE student_id = ?", conn, params=(student_id,))
    conn.close()
    return df

def get_activities(student_id: int) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM activities WHERE student_id = ?", conn, params=(student_id,))
    conn.close()
    return df

def get_career_requirements(role: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM career_requirements WHERE role = ?", conn, params=(role,))
    conn.close()
    return df

def get_all_career_roles() -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT role FROM career_requirements ORDER BY role ASC")
    roles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return roles

def add_skill(student_id: int, skill_name: str, category: str, proficiency: float):
    conn = get_connection()
    cursor = conn.cursor()
    # Check if skill exists for student
    cursor.execute("SELECT skill_id FROM skills WHERE student_id = ? AND LOWER(skill_name) = LOWER(?)", (student_id, skill_name))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("UPDATE skills SET proficiency = max(proficiency, ?), category = ? WHERE skill_id = ?",
                       (proficiency, category, existing[0]))
    else:
        cursor.execute("INSERT INTO skills (student_id, skill_name, category, proficiency) VALUES (?, ?, ?, ?)",
                       (student_id, skill_name, category, proficiency))
    conn.commit()
    conn.close()

def add_certificate(student_id: int, certificate_name: str, issuer: str, category: str, date_str: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO certificates (student_id, certificate_name, issuer, category, date) VALUES (?, ?, ?, ?, ?)",
        (student_id, certificate_name, issuer, category, date_str)
    )
    conn.commit()
    conn.close()

def get_recommendation_progress(student_id: int) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM recommendation_progress WHERE student_id = ?", conn, params=(student_id,))
    conn.close()
    return df

def update_recommendation_status(progress_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE recommendation_progress SET status = ? WHERE progress_id = ?", (status, progress_id))
    conn.commit()
    conn.close()

def save_recommendations(student_id: int, recs: List[Dict[str, str]]):
    conn = get_connection()
    cursor = conn.cursor()
    for rec in recs:
        # Avoid duplicate titles
        cursor.execute("SELECT progress_id FROM recommendation_progress WHERE student_id = ? AND title = ?", 
                       (student_id, rec['title']))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO recommendation_progress (student_id, title, priority, reason, status) VALUES (?, ?, ?, ?, ?)",
                (student_id, rec['title'], rec['priority'], rec['reason'], 'Pending')
            )
    conn.commit()
    conn.close()

def get_university_aggregate_stats() -> Dict[str, Any]:
    conn = get_connection()
    students_df = pd.read_sql_query("SELECT * FROM students", conn)
    records_df = pd.read_sql_query("SELECT * FROM academic_records", conn)
    skills_df = pd.read_sql_query("SELECT * FROM skills", conn)
    projects_df = pd.read_sql_query("SELECT * FROM projects", conn)
    internships_df = pd.read_sql_query("SELECT * FROM internships", conn)
    conn.close()

    total_students = len(students_df)
    avg_cgpa = round(students_df['cgpa'].mean(), 2) if total_students > 0 else 0.0

    # Low attendance risk (<75%)
    if not records_df.empty:
        low_att_students = records_df.groupby('student_id')['attendance'].mean()
        at_risk_count = (low_att_students < 75.0).sum()
    else:
        at_risk_count = 0

    internship_count = len(internships_df['student_id'].unique())
    project_count = len(projects_df['student_id'].unique())

    return {
        "total_students": total_students,
        "avg_cgpa": avg_cgpa,
        "at_risk_students": at_risk_count,
        "internship_participation_pct": round((internship_count / total_students * 100), 1) if total_students > 0 else 0.0,
        "project_participation_pct": round((project_count / total_students * 100), 1) if total_students > 0 else 0.0,
        "students_df": students_df,
        "skills_df": skills_df,
        "records_df": records_df,
        "projects_df": projects_df
    }
