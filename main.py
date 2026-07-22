import streamlit as st
import PyPDF2
import os
import io
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Analyzer", page_icon=":books:", layout="wide")  

st.title("AI Resume Analyzer")  
st.markdown("""
    Analyze resumes using **Google Gemini AI**.

### Features
- ATS Score
- Resume Summary
- Strengths & Weaknesses
- Missing Skills
- Interview Questions
- Improvement Suggestions
""")
st.divider()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

with st.sidebar:

    st.header("Job description")

    job_role = st.selectbox(
        "Select Target Job Role",
        [
            "Data Scientist",
            "Data Engineer",
            "Machine Learning Engineer",
            "Python Developer",
            "Software Engineer",
            "AI Engineer",
            "Other"
        ]
    )

    if job_role == "Other":
        job_role = st.text_input("Enter Custom Job Role")

    st.divider()

    st.header("Job Description")

    job_description = st.text_area(
        "Paste the Job Description here",
        height=250,
        placeholder="Paste the job description from LinkedIn, Naukri, Indeed..."
    )

uploaded_file = st.file_uploader("Upload a resume file or TXT", type=["pdf", "txt"])
# job_role = st.text_input("Enter your job role you are targeting(optional)")

analyze=st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")
if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        if not file_content.strip():
            st.error("The uploaded file is empty or could not be read.")
            st.stop()
            
        prompt = f"""Target Role:{job_role}

Job Description:
{job_description}

Resume:
{file_content}

Compare the resume against BOTH the selected role and the provided job description.

Return:

ATS Score:
<score>/100

Resume Match:
<percentage>%

Professional Summary:
<summary>

Strengths:
- item
- item

Weaknesses:
- item
- item

Technical Skills Found:
- item
- item

Missing Skills:
- item
- item

Missing Keywords:
- item
- item

Projects Evaluation:
<analysis>

Resume Formatting Review:
<analysis>

Learning Roadmap:
<analysis>

Improvement Suggestions:
- item
- item

Interview Questions:
1.
2.
3.
4.
5.

Hiring Recommendation:
<recommendation>
"""
        
        client = genai.Client(api_key=GOOGLE_API_KEY)
        # with st.spinner("🔍 Analyzing Resume... Please wait..."):   
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
)
        match = re.search(r"ATS Score\s*:\s*(\d+)", response.text)
        if match:
            score = int(match.group(1))
            st.metric("ATS Score", f"{score}/100")
            st.progress(score / 100)
        
        st.markdown("### Analysis Result")
        st.markdown(response.text)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# -------------------------------------------------------------------------------------
# Method 1: Open Your Project (Recommended)
# Step 1: Open the project folder
# Go to:
# C:\Users\Sweta kumari\Downloads\project2
# Open this folder.
# Step 2: Open Terminal
# Click on the folder path and type:
# cmd
# or
# powershell
# Then press Enter.
# A terminal will open directly inside your project folder.
# Step 3: Activate the virtual environment
# Type:
# .venv\Scripts\activate
# If you get a permission error, use:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
# Then run:
# .venv\Scripts\activate
# If activation is successful, you'll see:
# (project2) PS C:\Users\Sweta kumari\Downloads\project2>
# The (project2) at the beginning means your virtual environment is active.
# Step 4: Run the Streamlit app
# Type:
# streamlit run main.py
# You'll see output similar to:
# Local URL: http://localhost:8501
# Your browser will usually open automatically.
# If it doesn't, copy the URL and paste it into your browser.
# Next time you want to run it
# You only need these commands:
# cd C:\Users\Sweta kumari\Downloads\project2
# .venv\Scripts\activate
# streamlit run main.py
# That's it!
# If you close the terminal
# No problem.
# Next time:
# Open the project folder.
# Open PowerShell.
# Run:
# .venv\Scripts\activate
# Then:
# streamlit run main.py
# If Streamlit is already running
# Sometimes you'll see:
# Local URL: http://localhost:8501
# Just open:
# http://localhost:8501
# No need to run the app again unless you've stopped it.
# How to stop the app
# In the terminal, press:
# Ctrl + C
