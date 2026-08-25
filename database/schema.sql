-- Student360 AI Database Schema

CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    semester INTEGER NOT NULL,
    email TEXT NOT NULL,
    cgpa REAL NOT NULL,
    target_role TEXT NOT NULL,
    graduation_year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS academic_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course TEXT NOT NULL,
    marks REAL NOT NULL,
    grade TEXT NOT NULL,
    attendance REAL NOT NULL,
    semester INTEGER NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    category TEXT NOT NULL,
    proficiency REAL NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    project_name TEXT NOT NULL,
    description TEXT NOT NULL,
    domain TEXT NOT NULL,
    technologies TEXT NOT NULL,
    complexity TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    github_url TEXT NOT NULL,
    project_score REAL NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS certificates (
    certificate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    certificate_name TEXT NOT NULL,
    issuer TEXT NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS internships (
    internship_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    domain TEXT NOT NULL,
    duration TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS activities (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    activity_name TEXT NOT NULL,
    category TEXT NOT NULL,
    participation_level TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS career_requirements (
    role TEXT NOT NULL,
    skill TEXT NOT NULL,
    required_proficiency REAL NOT NULL,
    importance TEXT NOT NULL,
    PRIMARY KEY (role, skill)
);

CREATE TABLE IF NOT EXISTS recommendation_progress (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    priority TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending',
    FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
);
