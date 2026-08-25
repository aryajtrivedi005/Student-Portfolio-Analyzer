import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "student360.db")

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM recommendation_progress")
    cursor.execute("DELETE FROM activities")
    cursor.execute("DELETE FROM internships")
    cursor.execute("DELETE FROM certificates")
    cursor.execute("DELETE FROM projects")
    cursor.execute("DELETE FROM skills")
    cursor.execute("DELETE FROM academic_records")
    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM career_requirements")

    # 1. Seed Career Requirements
    career_reqs = [
        # Machine Learning Engineer
        ("Machine Learning Engineer", "Python", 85, "High"),
        ("Machine Learning Engineer", "Machine Learning", 85, "High"),
        ("Machine Learning Engineer", "SQL", 70, "Medium"),
        ("Machine Learning Engineer", "Docker", 65, "High"),
        ("Machine Learning Engineer", "Cloud", 60, "High"),
        ("Machine Learning Engineer", "MLOps", 60, "High"),
        ("Machine Learning Engineer", "Deep Learning", 75, "Medium"),
        ("Machine Learning Engineer", "REST API", 65, "Medium"),

        # Software Engineer
        ("Software Engineer", "Python", 80, "High"),
        ("Software Engineer", "Java", 75, "High"),
        ("Software Engineer", "Data Structures", 85, "High"),
        ("Software Engineer", "SQL", 75, "High"),
        ("Software Engineer", "Git", 80, "High"),
        ("Software Engineer", "REST API", 75, "Medium"),
        ("Software Engineer", "Docker", 60, "Medium"),
        ("Software Engineer", "System Design", 70, "Medium"),

        # Data Scientist
        ("Data Scientist", "Python", 85, "High"),
        ("Data Scientist", "Machine Learning", 85, "High"),
        ("Data Scientist", "SQL", 80, "High"),
        ("Data Scientist", "Statistics", 80, "High"),
        ("Data Scientist", "Data Visualization", 75, "Medium"),
        ("Data Scientist", "Deep Learning", 70, "Medium"),
        ("Data Scientist", "Big Data", 60, "Low"),

        # Data Analyst
        ("Data Analyst", "SQL", 85, "High"),
        ("Data Analyst", "Python", 75, "High"),
        ("Data Analyst", "Excel", 85, "High"),
        ("Data Analyst", "Data Visualization", 85, "High"),
        ("Data Analyst", "Statistics", 75, "Medium"),
        ("Data Analyst", "Power BI", 70, "Medium"),

        # Frontend Developer
        ("Frontend Developer", "JavaScript", 85, "High"),
        ("Frontend Developer", "React", 80, "High"),
        ("Frontend Developer", "HTML/CSS", 90, "High"),
        ("Frontend Developer", "TypeScript", 70, "Medium"),
        ("Frontend Developer", "Git", 75, "Medium"),
        ("Frontend Developer", "UI/UX Design", 70, "Medium"),

        # Backend Developer
        ("Backend Developer", "Python", 80, "High"),
        ("Backend Developer", "Node.js", 80, "High"),
        ("Backend Developer", "SQL", 85, "High"),
        ("Backend Developer", "REST API", 85, "High"),
        ("Backend Developer", "Docker", 70, "High"),
        ("Backend Developer", "System Design", 75, "Medium"),
        ("Backend Developer", "Redis", 60, "Low"),

        # Cloud Engineer
        ("Cloud Engineer", "AWS", 85, "High"),
        ("Cloud Engineer", "Docker", 85, "High"),
        ("Cloud Engineer", "Kubernetes", 75, "High"),
        ("Cloud Engineer", "Linux", 80, "High"),
        ("Cloud Engineer", "Python", 70, "Medium"),
        ("Cloud Engineer", "DevOps", 80, "High"),

        # Cybersecurity Analyst
        ("Cybersecurity Analyst", "Networking", 85, "High"),
        ("Cybersecurity Analyst", "Linux", 85, "High"),
        ("Cybersecurity Analyst", "Python", 75, "Medium"),
        ("Cybersecurity Analyst", "Cybersecurity Tools", 80, "High"),
        ("Cybersecurity Analyst", "Cryptography", 70, "Medium"),
        ("Cybersecurity Analyst", "Ethical Hacking", 75, "High")
    ]

    cursor.executemany(
        "INSERT INTO career_requirements (role, skill, required_proficiency, importance) VALUES (?, ?, ?, ?)",
        career_reqs
    )

    # 2. Seed Students
    # Student 1: Rahul Patel (DEMO STUDENT - ML Engineer target, high CGPA, strong Python/SQL/ML, missing Docker/Cloud/MLOps/Deployment)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (1, 'Rahul Patel', 'Computer Engineering', 7, 'rahul.patel@nirmauni.ac.in', 8.4, 'Machine Learning Engineer', 2025)
    """)

    # Student 2: Aarav Shah (Software Engineer, high CGPA, strong Java/DSA, weak project deployment & internships)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (2, 'Aarav Shah', 'Computer Engineering', 7, 'aarav.shah@nirmauni.ac.in', 9.1, 'Software Engineer', 2025)
    """)

    # Student 3: Riya Patel (Data Scientist, high CGPA, strong Python/ML/Stats, 1 internship, deployed NLP project)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (3, 'Riya Patel', 'Information Technology', 7, 'riya.patel@nirmauni.ac.in', 8.8, 'Data Scientist', 2025)
    """)

    # Student 4: Dev Mehta (Cloud Engineer, low CGPA, weak academics, but strong AWS/Docker/Kubernetes)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (4, 'Dev Mehta', 'Computer Engineering', 7, 'dev.mehta@nirmauni.ac.in', 7.2, 'Cloud Engineer', 2025)
    """)

    # Student 5: Ananya Joshi (Frontend Developer, high React/HTML/CSS, weak backend & DB)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (5, 'Ananya Joshi', 'Information Technology', 7, 'ananya.joshi@nirmauni.ac.in', 8.5, 'Frontend Developer', 2025)
    """)

    # Student 6: Neel Thakkar (Backend Developer, Node/Python/SQL, weak Docker & frontend)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (6, 'Neel Thakkar', 'Computer Engineering', 7, 'neel.thakkar@nirmauni.ac.in', 7.9, 'Backend Developer', 2025)
    """)

    # Student 7: Kavya Shah (Cybersecurity Analyst, strong Linux/Networking, missing Cloud)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (7, 'Kavya Shah', 'Information Technology', 7, 'kavya.shah@nirmauni.ac.in', 8.7, 'Cybersecurity Analyst', 2025)
    """)

    # Student 8: Aditya Desai (Data Analyst, strong SQL/Excel/Tableau, moderate academics)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (8, 'Aditya Desai', 'Computer Engineering', 7, 'aditya.desai@nirmauni.ac.in', 8.0, 'Data Analyst', 2025)
    """)

    # Student 9: Dhruv Patel (ML Engineer, low CGPA 6.8, attendance warning in Computer Networks < 70%, but strong ML skills)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (9, 'Dhruv Patel', 'Computer Engineering', 7, 'dhruv.patel@nirmauni.ac.in', 6.8, 'Machine Learning Engineer', 2025)
    """)

    # Student 10: Mira Shah (Software Engineer, ultra CGPA 9.5, zero projects deployed, zero internships)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (10, 'Mira Shah', 'Information Technology', 7, 'mira.shah@nirmauni.ac.in', 9.5, 'Software Engineer', 2025)
    """)

    # Student 11: Rohan Gupta (Data Scientist, certified in everything, 0 practical github evidence)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (11, 'Rohan Gupta', 'Computer Engineering', 7, 'rohan.gupta@nirmauni.ac.in', 8.2, 'Data Scientist', 2025)
    """)

    # Student 12: Tanvi Trivedi (Cloud Engineer, 2 internships, moderate skills, weak Kubernetes)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (12, 'Tanvi Trivedi', 'Information Technology', 7, 'tanvi.trivedi@nirmauni.ac.in', 8.0, 'Cloud Engineer', 2025)
    """)

    # Student 13: Yash Vora (Frontend Developer, low attendance risk <72%, high UI projects)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (13, 'Yash Vora', 'Computer Engineering', 7, 'yash.vora@nirmauni.ac.in', 7.4, 'Frontend Developer', 2025)
    """)

    # Student 14: Puja Shah (Backend Developer, Java/Spring Boot expert, 1 enterprise internship)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (14, 'Puja Shah', 'Computer Engineering', 7, 'puja.shah@nirmauni.ac.in', 8.6, 'Backend Developer', 2025)
    """)

    # Student 15: Harsh Solanki (ML Engineer, balanced mid-range profile)
    cursor.execute("""
        INSERT INTO students (student_id, name, department, semester, email, cgpa, target_role, graduation_year)
        VALUES (15, 'Harsh Solanki', 'Information Technology', 7, 'harsh.solanki@nirmauni.ac.in', 8.1, 'Machine Learning Engineer', 2025)
    """)


    # 3. Seed Academic Records
    courses = [
        "Data Structures & Algorithms",
        "Database Management Systems",
        "Computer Networks",
        "Operating Systems",
        "Machine Learning",
        "Software Engineering"
    ]

    # Student 1 (Rahul Patel) academic records - Attendance risk in Computer Networks!
    academic_data_rahul = [
        (1, "Data Structures & Algorithms", 86.0, "AA", 88.0, 6),
        (1, "Database Management Systems", 84.0, "AB", 85.0, 6),
        (1, "Computer Networks", 61.0, "CC", 69.0, 6),  # AT RISK (<75%) & LOW MARKS!
        (1, "Operating Systems", 78.0, "BB", 82.0, 6),
        (1, "Machine Learning", 92.0, "AA", 94.0, 7),
        (1, "Software Engineering", 80.0, "AB", 83.0, 7)
    ]
    cursor.executemany("INSERT INTO academic_records (student_id, course, marks, grade, attendance, semester) VALUES (?, ?, ?, ?, ?, ?)", academic_data_rahul)

    # Populate academic records for students 2-15
    generic_academics = []
    for sid in range(2, 16):
        base_mark = 55 + (sid * 2.5) % 35
        for course in courses:
            mark = min(98.0, max(50.0, round(base_mark + (hash(course + str(sid)) % 15 - 5), 1)))
            att = 92.0 if sid % 2 == 0 else (68.0 if course == "Computer Networks" and sid in [9, 13] else 81.0)
            grade = "AA" if mark >= 85 else ("AB" if mark >= 75 else ("BB" if mark >= 65 else "CC"))
            generic_academics.append((sid, course, mark, grade, att, 7))

    cursor.executemany("INSERT INTO academic_records (student_id, course, marks, grade, attendance, semester) VALUES (?, ?, ?, ?, ?, ?)", generic_academics)


    # 4. Seed Skills
    # Rahul Patel Skills (High Python/SQL/ML, Low Docker 35%, Low Cloud 25%, Low MLOps 10%)
    rahul_skills = [
        (1, "Python", "Programming", 90.0),
        (1, "SQL", "Database", 82.0),
        (1, "Machine Learning", "Machine Learning", 78.0),
        (1, "Deep Learning", "Machine Learning", 70.0),
        (1, "C++", "Programming", 65.0),
        (1, "Docker", "DevOps", 35.0),
        (1, "AWS", "Cloud", 25.0),
        (1, "MLOps", "DevOps", 10.0),
        (1, "Git", "Tools", 75.0)
    ]
    cursor.executemany("INSERT INTO skills (student_id, skill_name, category, proficiency) VALUES (?, ?, ?, ?)", rahul_skills)

    # Populate skills for other students
    other_skills = [
        # Student 2 (Aarav - Java/DSA)
        (2, "Java", "Programming", 92.0), (2, "Data Structures", "Programming", 90.0), (2, "SQL", "Database", 80.0), (2, "Git", "Tools", 85.0), (2, "Docker", "DevOps", 40.0),
        # Student 3 (Riya - Data Science)
        (3, "Python", "Programming", 92.0), (3, "Machine Learning", "Machine Learning", 88.0), (3, "SQL", "Database", 85.0), (3, "Statistics", "Data Science", 85.0), (3, "Deep Learning", "Machine Learning", 75.0),
        # Student 4 (Dev - Cloud)
        (4, "AWS", "Cloud", 90.0), (4, "Docker", "DevOps", 88.0), (4, "Kubernetes", "DevOps", 82.0), (4, "Linux", "Tools", 85.0), (4, "Python", "Programming", 65.0),
        # Student 5 (Ananya - Frontend)
        (5, "JavaScript", "Programming", 88.0), (5, "React", "Web Development", 85.0), (5, "HTML/CSS", "Web Development", 92.0), (5, "UI/UX Design", "Soft Skills", 80.0), (5, "SQL", "Database", 40.0),
        # Student 6 (Neel - Backend)
        (6, "Node.js", "Web Development", 85.0), (6, "Python", "Programming", 80.0), (6, "SQL", "Database", 88.0), (6, "REST API", "Web Development", 85.0), (6, "Docker", "DevOps", 45.0),
        # Student 7 (Kavya - Cyber)
        (7, "Networking", "Tools", 88.0), (7, "Linux", "Tools", 90.0), (7, "Cybersecurity Tools", "Tools", 82.0), (7, "Python", "Programming", 75.0), (7, "Cloud", "Cloud", 30.0),
        # Student 8 (Aditya - Analyst)
        (8, "SQL", "Database", 90.0), (8, "Excel", "Tools", 88.0), (8, "Data Visualization", "Data Science", 85.0), (8, "Python", "Programming", 70.0), (8, "Power BI", "Tools", 75.0),
        # Student 9 (Dhruv - ML)
        (9, "Python", "Programming", 88.0), (9, "Machine Learning", "Machine Learning", 82.0), (9, "SQL", "Database", 70.0), (9, "Docker", "DevOps", 20.0), (9, "Cloud", "Cloud", 15.0),
        # Student 10 (Mira - High GPA Software)
        (10, "Java", "Programming", 88.0), (10, "Python", "Programming", 85.0), (10, "SQL", "Database", 82.0), (10, "Data Structures", "Programming", 85.0),
        # Student 11 (Rohan - Certified Data Science)
        (11, "Python", "Programming", 80.0), (11, "Machine Learning", "Machine Learning", 82.0), (11, "SQL", "Database", 80.0), (11, "Deep Learning", "Machine Learning", 70.0),
        # Student 12 (Tanvi - Cloud)
        (12, "AWS", "Cloud", 82.0), (12, "Docker", "DevOps", 75.0), (12, "Linux", "Tools", 78.0), (12, "Python", "Programming", 70.0),
        # Student 13 (Yash - Frontend)
        (13, "JavaScript", "Programming", 85.0), (13, "React", "Web Development", 82.0), (13, "HTML/CSS", "Web Development", 88.0),
        # Student 14 (Puja - Backend)
        (14, "Java", "Programming", 90.0), (14, "REST API", "Web Development", 88.0), (14, "SQL", "Database", 85.0), (14, "Docker", "DevOps", 65.0),
        # Student 15 (Harsh - ML)
        (15, "Python", "Programming", 82.0), (15, "Machine Learning", "Machine Learning", 80.0), (15, "SQL", "Database", 75.0), (15, "Docker", "DevOps", 40.0)
    ]
    cursor.executemany("INSERT INTO skills (student_id, skill_name, category, proficiency) VALUES (?, ?, ?, ?)", other_skills)


    # 5. Seed Projects
    # Rahul Patel Projects (Spam Shield - local, Sentiment - local. NO DEPLOYMENT!)
    rahul_projects = [
        (1, "Spam Shield NLP", "Email spam classification using scikit-learn Naive Bayes and TF-IDF NLP pipeline.",
         "Machine Learning", "Python, Machine Learning, Scikit-Learn, Pandas", "Medium", "Local Only",
         "https://github.com/rahulpatel/spam-shield", 78.0),
        (1, "Customer Churn Predictor", "Predictive model for telecom customer churn using Random Forest with feature importances.",
         "Data Science", "Python, Scikit-Learn, Matplotlib, SQL", "Medium", "Local Only",
         "https://github.com/rahulpatel/churn-prediction", 74.0)
    ]
    cursor.executemany("""
        INSERT INTO projects (student_id, project_name, description, domain, technologies, complexity, deployment_status, github_url, project_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rahul_projects)

    # Projects for other students
    other_projects = [
        (2, "AlgoVisualizer", "Interactive web tool for algorithm visualization in Java", "Software Engineering", "Java, Swing, Algorithms", "High", "Local Only", "https://github.com/aarav/algo-vis", 80.0),
        (3, "Medical Imaging Brain Tumor Classifier", "CNN model deployed on Streamlit Cloud for MRI brain tumor detection", "Machine Learning", "Python, TensorFlow, Streamlit, Docker", "Advanced", "Deployed", "https://github.com/riya/brain-mri", 92.0),
        (4, "Multi-Region Kubernetes Cluster Infra", "Terraform IAC script setting up AWS EKS cluster with Prometheus monitoring", "Cloud", "AWS, Terraform, Kubernetes, Docker, Prometheus", "Advanced", "Deployed", "https://github.com/dev/aws-eks-iac", 95.0),
        (5, "DesignSystem UI Library", "Component library built with React & Tailwind CSS", "Web Development", "React, JavaScript, HTML/CSS, Tailwind", "Medium", "Deployed", "https://github.com/ananya/ui-lib", 85.0),
        (6, "E-Commerce REST Microservices", "Express.js REST APIs with JWT authentication & MongoDB", "Web Development", "Node.js, Express, MongoDB, REST API", "High", "Deployed", "https://github.com/neel/shop-api", 86.0),
        (7, "Network Vulnerability Scanner", "Python port scanner & CVE lookup automated tool", "Cybersecurity", "Python, Networking, Linux, Scapy", "High", "Local Only", "https://github.com/kavya/vuln-scan", 82.0),
        (8, "Sales Performance Interactive Dashboard", "SQL data pipeline and Tableau executive reporting dashboard", "Data Analytics", "SQL, Tableau, Excel, Python", "Medium", "Deployed", "https://github.com/aditya/sales-dash", 84.0),
        (9, "Object Detection Robot Vision", "YOLOv8 real-time object identification pipeline", "Computer Vision", "Python, OpenCV, PyTorch", "High", "Local Only", "https://github.com/dhruv/yolo-vision", 76.0),
        (10, "Library Management System", "Console application for book cataloging", "Software Engineering", "Java, MySQL", "Low", "Local Only", "https://github.com/mira/library-app", 60.0),
        (11, "House Price Prediction Model", "Jupyter notebook exploring linear regression", "Machine Learning", "Python, Pandas, Scikit-Learn", "Low", "Local Only", "https://github.com/rohan/house-price", 55.0),
        (12, "Cloud Native Microservice Deployment", "Dockerized microservices deployed on AWS EC2", "Cloud", "AWS, Docker, Python", "High", "Deployed", "https://github.com/tanvi/cloud-app", 88.0),
        (13, "Portfolio Website", "Personal website built with React & Framer Motion", "Web Development", "React, HTML/CSS, JavaScript", "Medium", "Deployed", "https://github.com/yash/my-portfolio", 81.0),
        (14, "Bank Transaction Processing API", "High-throughput Java Spring Boot REST service", "Software Engineering", "Java, Spring Boot, PostgreSQL, Docker", "Advanced", "Deployed", "https://github.com/puja/bank-api", 90.0),
        (15, "Sentiment Analysis API", "FastAPI microservice serving BERT sentiment model", "Machine Learning", "Python, PyTorch, FastAPI", "Medium", "Local Only", "https://github.com/harsh/sentiment-api", 79.0)
    ]
    cursor.executemany("""
        INSERT INTO projects (student_id, project_name, description, domain, technologies, complexity, deployment_status, github_url, project_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, other_projects)


    # 6. Seed Certificates
    # Rahul Patel Certificates
    rahul_certs = [
        (1, "Machine Learning Specialization", "Coursera / Stanford", "Machine Learning", "2024-03-15"),
        (1, "Complete Python Bootcamp", "Udemy", "Programming", "2023-11-10")
    ]
    cursor.executemany("INSERT INTO certificates (student_id, certificate_name, issuer, category, date) VALUES (?, ?, ?, ?, ?)", rahul_certs)

    other_certs = [
        (3, "Deep Learning Specialization", "DeepLearning.AI", "Machine Learning", "2024-01-20"),
        (4, "AWS Certified Solutions Architect - Associate", "Amazon Web Services", "Cloud", "2024-04-10"),
        (5, "Meta Front-End Developer Certificate", "Coursera", "Web Development", "2023-09-05"),
        (6, "Node.js Application Development", "Linux Foundation", "Web Development", "2024-02-18"),
        (7, "CompTIA Security+", "CompTIA", "Cybersecurity", "2023-12-01"),
        (8, "Google Data Analytics Professional", "Coursera", "Data Analytics", "2024-03-01"),
        (11, "IBM Data Science Professional Certificate", "Coursera", "Data Science", "2024-05-12"),
        (11, "AWS Cloud Practitioner", "Amazon Web Services", "Cloud", "2024-06-01"),
        (14, "Oracle Certified Professional: Java SE 17", "Oracle", "Programming", "2024-01-15")
    ]
    cursor.executemany("INSERT INTO certificates (student_id, certificate_name, issuer, category, date) VALUES (?, ?, ?, ?, ?)", other_certs)


    # 7. Seed Internships
    # Rahul Patel has NO INTERNSHIP! (Significant gap for ML Engineer role)
    other_internships = [
        (3, "TCS", "Data Science Intern", "Machine Learning & AI", "3 Months (Summer 2024)"),
        (4, "Cloud Native Labs", "DevOps Intern", "Cloud Infrastructure", "6 Months (Jan-Jun 2024)"),
        (6, "TechCorp Solutions", "Backend Developer Intern", "Software Development", "3 Months (Summer 2024)"),
        (8, "Analytica Insights", "Data Analyst Intern", "Business Intelligence", "2 Months (Winter 2023)"),
        (12, "Infosys", "Cloud Computing Intern", "Cloud Services", "3 Months (Summer 2024)"),
        (14, "Barclays Technology", "Software Engineering Intern", "FinTech", "2 Months (Summer 2024)")
    ]
    cursor.executemany("INSERT INTO internships (student_id, company, role, domain, duration) VALUES (?, ?, ?, ?, ?)", other_internships)


    # 8. Seed Activities
    activities = [
        (1, "Google Developer Student Club (GDSC)", "Technical Community", "Core Member", "2023-2024"),
        (1, "Nirma TechFest Codeathon", "Competition", "Participant", "2024-02"),
        (2, "ACM Student Chapter", "Technical Community", "President", "2023-2024"),
        (3, "AI Research Club", "Research", "Lead Researcher", "2023-2024"),
        (4, "Open Source Club", "Community", "Maintainer", "2023-2024"),
        (5, "Design & UI Club", "Creative", "Vice Lead", "2023-2024")
    ]
    cursor.executemany("INSERT INTO activities (student_id, activity_name, category, participation_level, date) VALUES (?, ?, ?, ?, ?)", activities)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully!")
