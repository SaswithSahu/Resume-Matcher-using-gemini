# 🤖 Resume Matcher - LLM-powered Smart Matching Tool

A smart **Resume Matcher** web app built using **Gemini**, **LangChain**, and **Streamlit**, designed to extract, parse, and match resumes with job descriptions in real-time. It calculates a total experience score and provides an intelligent match percentage to assist in recruitment workflows.

---

## 🔧 Tech Stack

- **🧠 Gemini (Google)**: LLM for extracting structured data
- **🛠️ LangChain**: Used `with_structured_output()` to extract clean structured info
- **📄 PDF/DOCX Parsing**: Extracts resume data from file uploads
- **🌐 Streamlit**: Fast and interactive UI
- **🧮 Matching Engine**: Skill, experience, and education comparison
- **✨ Experience Calculation**: Total work experience derived from timeline

---

## 🚀 Features

- Upload resumes in `.pdf` or `.docx` format
- Paste job descriptions directly in the app
- Extract:
  - Full Name
  - Email
  - Phone Number
  - Skills (as a list)
  - Total Experience (auto-calculated)
  - Education Summary
- Compute:
  - **Match Percentage** based on skill overlap
  - **Experience Match**
  - **Education Relevance**
- Built-in data parser using `with_structured_output()` in LangChain for structured and reliable output

---

## 📸 Demo Preview

![screenshot](path_to_screenshot.png)

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/resume-matcher.git
cd resume-matcher

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
