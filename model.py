from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic.v1 import BaseModel, Field  # ✅ Use pydantic.v1 for compatibility
from dotenv import load_dotenv

load_dotenv()

# Define output schema
class DataReq(BaseModel):
    name: str
    email: str
    phone: str
    skills: list[str]
    experience: str
    education: str

# Load Gemini model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

# Use structured output
structured_model = model.with_structured_output(DataReq)

# Sample Resume
resume = """
Saswith Sahu  
Email: saswith@example.com  
Phone: +91-9876543210  
Experience: 2 years as a MERN stack developer  
Skills: React, Node.js, Express, MongoDB, JavaScript, HTML, CSS  
Education: MCA - Master of Computer Applications
"""

# Sample JD
jd = """
We are hiring a full-stack web developer with at least 1.5 years of experience.
The candidate must be proficient in React and Node.js.
Should be comfortable working with MongoDB and Express.
Preferred qualifications include an MCA or B.Tech degree.
"""

# Prompt for Resume
resume_prompt = f"""
Extract the following fields from the RESUME:

- Name
- Email
- Phone number
- Skills (as list)
- Experience
- Education

RESUME:
{resume}
"""

# Prompt for JD
jd_prompt = f"""
Extract the following requirements from the JOB DESCRIPTION:

- Name (optional)
- Email (optional)
- Phone number (optional)
- Skills (as list)
- Experience
- Education

JOB DESCRIPTION:
{jd}
"""

# Invoke both separately
resume_data = structured_model.invoke(resume_prompt)
jd_data = structured_model.invoke(jd_prompt)

# Normalize skills
normalize = lambda skills: set(s.lower().strip('"').strip("'").strip() for s in skills)
resume_skills = normalize(resume_data.skills)
jd_skills = normalize(jd_data.skills)

# Compare skills
common_skills = resume_skills & jd_skills
missing_skills = jd_skills - resume_skills
match_percentage = (len(common_skills) / len(jd_skills)) * 100 if jd_skills else 0

# Final Output
print("\n🔍 Comparison Results:")
print("✅ Common Skills:", list(common_skills))
print("❌ Missing Skills:", list(missing_skills))
print("📊 Match Percentage:", f"{match_percentage:.2f}%")
print("📆 Resume Experience:", resume_data.experience)
print("📆 JD Experience Required:", jd_data.experience)
print("🎓 Resume Education:", resume_data.education)
print("🎓 JD Education Required:", jd_data.education)
