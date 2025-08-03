import streamlit as st
import os
import pdfplumber
import docx
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

# Load .env variables
load_dotenv()

# Initialize Gemini model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

# Define output schemas
class ResumeData(BaseModel):
    name: str
    email: str
    phone: str
    skills: list[str]
    experience: str  # e.g., "2 years"
    education: str   # e.g., "MCA (2022)"

class JDData(BaseModel):
    skills: list[str]
    experience: str  # e.g., "1.5 years"
    education: str   # e.g., "B.Tech or MCA"

# Enable structured output
resume_model = model.with_structured_output(ResumeData)
jd_model = model.with_structured_output(JDData)

# File parsing
def extract_text_from_file(file):
    ext = os.path.splitext(file.name)[-1].lower()
    if ext == ".pdf":
        with pdfplumber.open(file) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif ext == ".docx":
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return None

# Streamlit UI
st.set_page_config(page_title="Resume Matcher", layout="centered")
st.title("📄 Resume Matcher using Gemini AI")
st.markdown("Upload your **resume (PDF or DOCX)** and paste the **job description** to get a smart comparison.")

resume_file = st.file_uploader("📤 Upload Resume", type=["pdf", "docx"])
jd_text = st.text_area("📝 Paste Job Description")

if st.button("🔍 Analyze"):
    if not resume_file or not jd_text.strip():
        st.warning("⚠️ Please upload a resume and paste the job description.")
    else:
        with st.spinner("🔍 Processing..."):
            resume_text = extract_text_from_file(resume_file)

            if not resume_text:
                st.error("❌ Could not extract text from the uploaded resume.")
            else:
                # Enhanced prompts
                resume_prompt = f"""
                From the following RESUME text, extract and return the below fields in structured format. Make sure to:

                - Calculate total combined professional experience by summing up durations across all job roles (not just the latest).
                - Return the total experience in a human-readable format like: "1 year 8 months" or "2 years".
                - For education, extract only the highest qualification and include passing year if mentioned.

                Extract:

                - Name: Full candidate name
                - Email: Valid professional email ID
                - Phone: 10-digit or international format
                - Skills: List of technical skills, tools, or technologies mentioned
                - Experience: Total combined work experience across all roles (e.g., "1 year 8 months")
                - Education: Highest qualification with specialization and passing year if present (e.g., "MCA - Data Science (2025)")

                RESUME:
                {resume_text}
                """

                jd_prompt = f"""
                Extract the following structured fields from the job description below:
                - Skills (as a list)
                - Experience (minimum years required, e.g., "1.5 years")
                - Education (qualification required, e.g., "B.Tech or MCA")

                JOB DESCRIPTION:
                {jd_text}
                """

                try:
                    resume_data = resume_model.invoke(resume_prompt)
                    jd_data = jd_model.invoke(jd_prompt)

                    # Normalize skill sets
                    normalize = lambda skills: set(s.lower().strip('"').strip("'").strip() for s in skills)
                    resume_skills = normalize(resume_data.skills)
                    jd_skills = normalize(jd_data.skills)

                    common_skills = sorted(resume_skills & jd_skills)
                    missing_skills = sorted(jd_skills - resume_skills)
                    match_percentage = (len(common_skills) / len(jd_skills)) * 100 if jd_skills else 0

                    # Display output
                    st.success("✅ Analysis Completed")
                    st.markdown("### 🔍 Comparison Results")
                    st.write(f"**✅ Common Skills:** {common_skills}")
                    st.write(f"**❌ Missing Skills:** {missing_skills}")
                    st.write(f"**📊 Match Percentage:** {match_percentage:.2f}%")

                    st.markdown("---")
                    st.markdown("### 📆 Experience")
                    st.write(f"**Resume:** {resume_data.experience}")
                    st.write(f"**JD Required:** {jd_data.experience}")

                    st.markdown("### 🎓 Education")
                    st.write(f"**Resume:** {resume_data.education}")
                    st.write(f"**JD Required:** {jd_data.education}")

                except Exception as e:
                    st.error(f"❌ AI processing error: {e}")
