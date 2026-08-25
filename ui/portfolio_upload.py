import streamlit as st
from document_processing.document_parser import extract_text_from_file
from document_processing.ocr import perform_ocr
from document_processing.portfolio_extractor import extract_certificate_data, extract_resume_data
from database.database import add_certificate, add_skill

def render_portfolio_upload(student_id: int, student_name: str):
    st.markdown("## 📄 Portfolio Document & Certificate OCR Upload")
    st.markdown(f"Upload certificates or resumes to automatically extract skills and update **{student_name}'s** profile in real-time.")

    upload_type = st.radio("Select Document Type", ["Certificate (Image/PDF)", "Resume (PDF/Text)"], horizontal=True)

    if upload_type == "Certificate (Image/PDF)":
        st.markdown("### 📜 Certificate OCR Scanner")
        uploaded_file = st.file_uploader("Choose a certificate image (PNG, JPG) or PDF", type=["png", "jpg", "jpeg", "pdf"])

        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            filename = uploaded_file.name

            with st.spinner("Extracting certificate text via OpenCV & PyTesseract..."):
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    extracted_text = perform_ocr(bytes_data)
                else:
                    extracted_text = extract_text_from_file(bytes_data, filename)

                cert_info = extract_certificate_data(extracted_text)

            st.success("✅ Certificate scanned and parsed successfully!")

            col_img, col_info = st.columns([1, 1])

            with col_img:
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    st.image(bytes_data, caption="Uploaded Certificate", use_container_width=True)
                else:
                    st.info(f"📄 PDF Document: {filename}")

            with col_info:
                st.markdown("#### Detected Certificate Metadata")
                cert_name = st.text_input("Certificate Name", value=cert_info['certificate_name'])
                issuer = st.text_input("Issuer", value=cert_info['issuer'])
                category = st.selectbox("Category", ["Machine Learning", "Cloud", "Web Development", "Database", "Programming", "Technical"], index=0)
                cert_date = st.text_input("Issue Date", value=cert_info['date'])
                skills_found = st.text_input("Extracted Skills (comma separated)", value=", ".join(cert_info['skills']))

                if st.button("➕ Add Certificate & Skills to Portfolio", type="primary"):
                    add_certificate(student_id, cert_name, issuer, category, cert_date)
                    for sk in [s.strip() for s in skills_found.split(',') if s.strip()]:
                        add_skill(student_id, sk, category, 75.0)

                    st.balloons()
                    st.success(f"Added '{cert_name}' to {student_name}'s database record! Click Re-analyze to update scores.")
                    st.rerun()

    else:
        st.markdown("### 📝 Resume Skill Consistency Analyzer")
        uploaded_file = st.file_uploader("Upload Resume PDF or Text file", type=["pdf", "txt"])

        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            filename = uploaded_file.name

            with st.spinner("Analyzing resume content..."):
                extracted_text = extract_text_from_file(bytes_data, filename)
                resume_info = extract_resume_data(extracted_text)

            st.success(f"✅ Resume analyzed! Consistency Score: {resume_info['consistency_score']}%")

            st.markdown("#### Extracted Resume Skills")
            skills_str = ", ".join(resume_info['extracted_skills'])
            st.info(f"**Found Skills:** {skills_str}")

            if st.button("➕ Sync Resume Skills to Portfolio", type="primary"):
                for sk in resume_info['extracted_skills']:
                    add_skill(student_id, sk, "Technical", 75.0)
                st.balloons()
                st.success("Synced resume skills to SQLite database!")
                st.rerun()
