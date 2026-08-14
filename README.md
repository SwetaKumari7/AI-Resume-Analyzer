# 🤖 AI Resume Analyzer

An AI-powered resume analysis tool built with **Python, Streamlit, and Google Gemini AI**. The application evaluates a resume against a selected job role and job description, then provides an ATS score, resume match percentage, skills analysis, missing keywords, improvement suggestions, interview questions, and a hiring recommendation.

## ✨ Features

* 📄 Upload resumes in **PDF or TXT** format
* 🎯 Select a target job role
* 📝 Paste a job description for comparison
* 🤖 Analyze resumes using **Google Gemini AI**
* 📊 Generate an **ATS Score out of 100**
* 📈 Calculate **Resume Match percentage**
* 📋 Generate a professional resume summary
* 💪 Identify resume strengths
* ⚠️ Identify weaknesses and improvement areas
* 🛠️ Extract technical skills from the resume
* 🔎 Identify missing skills
* 🔑 Detect missing keywords from the job description
* 🚀 Evaluate projects mentioned in the resume
* 📑 Review resume formatting
* 🗺️ Generate a learning roadmap
* 💡 Provide resume improvement suggestions
* 🎤 Generate interview questions
* 👔 Provide an AI-based hiring recommendation

## 🧠 How It Works

The application follows a simple AI-powered workflow:

```text
        Upload Resume
              ↓
       PDF/TXT Extraction
              ↓
       Select Target Role
              ↓
    Add Job Description
              ↓
        Gemini AI Analysis
              ↓
     Resume vs Job Matching
              ↓
       ATS & Match Score
              ↓
 ┌───────────────────────────┐
 │ Strengths & Weaknesses    │
 │ Technical Skills          │
 │ Missing Skills            │
 │ Missing Keywords          │
 │ Project Evaluation        │
 │ Formatting Review         │
 │ Learning Roadmap          │
 │ Improvement Suggestions   │
 │ Interview Questions       │
 │ Hiring Recommendation     │
 └───────────────────────────┘
```

## 🛠️ Tech Stack

| Technology           | Purpose                                   |
| -------------------- | ----------------------------------------- |
| **Python**           | Core programming language                 |
| **Streamlit**        | Web application interface                 |
| **Google Gemini AI** | Resume analysis and AI-generated feedback |
| **PyPDF2**           | Extracting text from PDF resumes          |
| **python-dotenv**    | Managing environment variables            |
| **Regex (re)**       | Extracting the ATS score from AI output   |
| **Git & GitHub**     | Version control and project hosting       |

The project's dependency configuration specifies Python 3.13+ along with Streamlit, Google GenAI, PyPDF2, python-dotenv, and related packages.

## 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── main.py
├── pyproject.toml
├── uv.lock
├── README.md
│
├── Screenshot 2026-07-22 201331.png
└── Screenshot 2026-07-22 201353.png
```

The main application logic is contained in `main.py`.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/SwetaKumari7/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\activate
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

If you are using the project's `pyproject.toml`/`uv.lock` workflow, install the dependencies according to your preferred Python environment manager.

## 🔐 API Key Configuration

This project uses the **Google Gemini API** for AI-powered resume analysis.

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

**Important:** Never upload your `.env` file or API key to GitHub.

The application loads the API key from the environment using `python-dotenv`.

## ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run main.py
```

After starting the application, Streamlit will provide a local URL, normally:

```text
http://localhost:8501
```

Open the URL in your browser.

## 🖥️ Using the Application

### Step 1 — Select a Job Role

Choose the role you are targeting, such as:

* Data Scientist
* Data Engineer
* Machine Learning Engineer
* Python Developer
* Software Engineer
* AI Engineer
* Other

You can also enter a custom job role.

### Step 2 — Add the Job Description

Paste the job description into the provided text area.

This allows the AI to compare the resume with the actual requirements of the position.

### Step 3 — Upload Your Resume

Upload either:

```text
PDF
TXT
```

The application extracts the resume text before sending it for analysis.

### Step 4 — Analyze

Click:

```text
Analyze Resume
```

The application sends the resume, target role, and job description to Gemini AI for analysis.

### Step 5 — Review the Results

The application displays the generated analysis, including:

* ATS Score
* Resume Match
* Professional Summary
* Strengths
* Weaknesses
* Technical Skills
* Missing Skills
* Missing Keywords
* Projects Evaluation
* Resume Formatting Review
* Learning Roadmap
* Improvement Suggestions
* Interview Questions
* Hiring Recommendation

The ATS score is also displayed as a visual progress indicator.

## 📊 Example Output

```text
ATS Score: 82/100

Resume Match: 78%

Strengths:
- Python programming
- Machine learning projects
- SQL knowledge

Missing Skills:
- Docker
- AWS
- CI/CD

Missing Keywords:
- REST API
- Cloud Computing
- Kubernetes

Improvement Suggestions:
- Add measurable project achievements
- Improve technical skill alignment
- Add relevant keywords from the job description

Interview Questions:
1. Explain your most relevant project.
2. How do you use Python in your projects?
3. Explain your experience with SQL.
4. How would you deploy a machine learning model?
5. Why are you suitable for this role?
```

*The actual output depends on the uploaded resume, selected role, and job description.*

## 🎯 Project Objective

The goal of this project is to demonstrate how **Generative AI and document processing** can be applied to a practical career-related problem.

Instead of manually comparing a resume with a job description, the application uses AI to identify relevant skills, gaps, keywords, and areas for improvement.

## 🔮 Future Improvements

Possible future enhancements include:

* [ ] Job description matching with more advanced semantic similarity
* [ ] Resume section-wise scoring
* [ ] Resume keyword optimization
* [ ] Support for DOCX resumes
* [ ] Resume improvement/rewrite feature
* [ ] Downloadable analysis report
* [ ] Resume version comparison
* [ ] Job recommendation based on resume skills
* [ ] Skill-gap visualization
* [ ] User history and saved analyses
* [ ] Deployment as a public web application

## ⚠️ Limitations

* The analysis depends on the quality of the extracted resume text.
* ATS scores are AI-generated estimates and should not be treated as an official ATS score.
* Results may vary depending on the resume and job description provided.
* The application currently supports PDF and TXT resume files.
* A valid Google Gemini API key is required for AI analysis.

## 🔒 Security

Do not commit sensitive information such as:

```text
.env
API keys
Passwords
Personal access tokens
```

Add `.env` to `.gitignore` before pushing the project to GitHub.

## 👩‍💻 Author

**Sweta Kumari**

B.Tech — Information Technology

GitHub: [@SwetaKumari7](https://github.com/SwetaKumari7)

## ⭐ Support

If you found this project useful, consider giving the repository a ⭐ on GitHub.

---

### 📌 Project Highlights

**AI Resume Analyzer** demonstrates practical use of:

`Python` • `Streamlit` • `Generative AI` • `Google Gemini` • `PDF Processing` • `NLP` • `Resume Analysis` • `ATS Evaluation`
