#  AI Resume Analyzer & ATS Checker

> **"Tomorrow is my TCS NQT exam, but instead of studying... I built an AI Resume Analyzer. 😅"**
> *Hopefully this project impresses recruiters as much as my exam answers!*

---

##  Overview

AI Resume Analyzer is an intelligent web application built using **Python**, **Streamlit**, and **Google Gemini AI**. It helps job seekers evaluate their resumes by comparing them against a target job role and optional job description, providing an ATS score, skill gap analysis, personalized suggestions, interview questions, and hiring recommendations.

This project demonstrates the practical application of **Generative AI**, **Prompt Engineering**, **PDF Processing**, and **Streamlit Web Development**.

---

##  Features

*  Upload Resume (PDF/TXT)
*  Analyze Resume for Any Job Role
*  Compare Resume with Job Description
*  ATS Score (0–100)
*  Resume Match Percentage
*  Strengths & Weaknesses Analysis
*  Missing Skills Detection
*  Missing Keywords Identification
*  Personalized Improvement Suggestions
*  Learning Roadmap
*  AI-Generated Interview Questions
*  Hiring Recommendation
*  Powered by Google Gemini AI

---

#  Why This Project?

Recruiters often use **Applicant Tracking Systems (ATS)** to filter resumes before a human even sees them.

This application helps candidates:

* Understand how ATS evaluates resumes.
* Identify missing technical skills and keywords.
* Improve resume quality for a specific job role.
* Prepare for interviews with AI-generated questions.
* Receive actionable suggestions to increase their chances of getting shortlisted.

Instead of guessing why a resume gets rejected, this project provides intelligent AI-based feedback within seconds.

---

#  Advantages

✅ Saves time by instantly analyzing resumes.

✅ Helps improve ATS compatibility.

✅ Identifies missing skills for the target role.

✅ Suggests personalized improvements.

✅ Generates interview questions based on the resume.

✅ Compares resumes against real job descriptions.

✅ Beginner-friendly and easy to use.

✅ Built with modern AI technologies.

---

# 🛠 Tech Stack

* Python
* Streamlit
* Google Gemini AI API
* PyPDF2
* Python-dotenv

---

#  Project Structure

```text
AI-Resume-Analyzer/
│
├── main.py
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/AI-Resume-Analyzer.git
```

### 2️⃣ Navigate to the Project

```bash
cd AI-Resume-Analyzer
```

### 3️⃣ Create Virtual Environment

#### Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Create `.env`

Create a file named **.env**

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

### 6️⃣ Get Gemini API Key

1. Visit Google AI Studio.
2. Log in with your Google account.
3. Generate an API Key.
4. Copy the key.
5. Paste it into your `.env` file.

---

### 7️⃣ Run the Application

```bash
streamlit run main.py
```

Open the URL displayed in your terminal (usually `http://localhost:8501`).

---

# 📖 How to Use

1. Upload your resume (PDF/TXT).
2. Select or enter the target job role.
3. (Optional) Paste the job description.
4. Click **Analyze Resume**.
5. View the AI-generated analysis.

The report includes:

* ATS Score
* Resume Match %
* Professional Summary
* Strengths
* Weaknesses
* Missing Skills
* Missing Keywords
* Learning Roadmap
* Improvement Suggestions
* Interview Questions
* Hiring Recommendation

---

#  Requirements

```text
streamlit
google-genai
PyPDF2
python-dotenv
```

---

#  .gitignore

```text
.venv/
__pycache__/
.env
*.pyc
```

---

#  Future Enhancements

*  Export Analysis as PDF
*  Interactive Dashboard
*  AI Resume Chat Assistant
*  Dark Mode
*  Resume History
*  Multi-language Support
*  LinkedIn Profile Analysis

---

#  Skills Demonstrated

This project showcases:

* Python Programming
* Prompt Engineering
* Generative AI Integration
* Streamlit Development
* PDF Processing
* API Integration
* Environment Variable Management
* Resume Analysis Logic
* User Interface Design

---

#  Author

**Sweta Kumari**

B.Tech in Information Technology

Passionate about Artificial Intelligence, Machine Learning, Software Development, and solving real-world problems using AI.

---

#  If You Like This Project

If you found this project useful, consider giving it a ⭐ on GitHub.

It motivates me to build more AI-powered applications and continue learning.

---

> **"Built with ☕, curiosity, and a little bit of pre-exam panic(tcs nqt exam (23 july 2026)."** 
